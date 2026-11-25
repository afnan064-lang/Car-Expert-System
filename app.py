"""Vehicle Troubleshooting Expert System - Streamlit app."""
import pandas as pd
import streamlit as st

from inference_engine import InferenceEngine
from knowledge_base import (ASSERTIONS, DIAGNOSES, RULES, SEVERITY_ICON, SYMPTOMS,
                            SYMPTOM_CATEGORY)
from nlp import extract_symptoms

st.set_page_config(page_title="Vehicle Troubleshooting Expert System", page_icon="🚗", layout="wide")
engine = InferenceEngine()

# ---------- session state ----------
ss = st.session_state
ss.setdefault("messages", [{"role": "assistant",
                            "content": "Hello! Describe what is wrong with your vehicle "
                                       "(e.g. *\"engine won't start and the dashboard lights are dim\"*)."}])
ss.setdefault("chat_syms", set())   # symptoms found in chat text
ss.setdefault("yes", set())         # follow-up questions answered Yes
ss.setdefault("no", set())          # follow-up questions answered No
ss.setdefault("manual", [])         # symptoms picked in the sidebar


def reset():
    ss.messages = ss.messages[:1]
    ss.chat_syms, ss.yes, ss.no, ss.manual = set(), set(), set(), []


# ---------- sidebar ----------
with st.sidebar:
    st.header("🔧 Pick symptoms")
    st.multiselect("Search and select symptoms", SYMPTOMS, key="manual",
                   format_func=lambda s: f"{s}  ·  {SYMPTOM_CATEGORY[s]}")
    st.button("🔄 Start new diagnosis", on_click=reset, width="stretch")
    st.divider()
    st.caption(f"Knowledge base: **{len(RULES)} rules** · **{len(ASSERTIONS)} assertions** "
               f"({len(SYMPTOMS)} symptoms + {len(DIAGNOSES)} diagnoses)")

# working memory = every symptom the user has confirmed
facts = (ss.chat_syms | ss.yes | set(ss.manual)) - ss.no
fired, memory = engine.forward_chain(facts)

st.title("🚗 Vehicle Troubleshooting Expert System")
tab_diag, tab_kb, tab_about = st.tabs(["Diagnose", "Knowledge base", "About"])

# ---------- Diagnose tab ----------
with tab_diag:
    left, right = st.columns([3, 2], gap="large")

    with left:
        for m in ss.messages:
            with st.chat_message(m["role"]):
                st.markdown(m["content"])

        text = st.chat_input("Describe the problem with your vehicle...")
        if text:
            found = extract_symptoms(text)
            ss.messages.append({"role": "user", "content": text})
            if found:
                ss.chat_syms.update(found)
                reply = "I understood these symptoms:\n" + "\n".join(f"- {s}" for s in found)
            else:
                reply = ("I couldn't match that to a known symptom. Try describing a sound, smell, "
                         "warning light or behaviour, or pick symptoms from the sidebar.")
            ss.messages.append({"role": "assistant", "content": reply})
            st.rerun()

    with right:
        st.subheader("Current symptoms")
        if facts:
            for s in sorted(facts):
                st.markdown(f"- {s}")
        else:
            st.caption("None yet.")

        st.subheader("Diagnosis")
        if fired:
            for rule in sorted(fired, key=lambda r: ["Critical", "High", "Medium", "Low"].index(r.severity)):
                with st.container(border=True):
                    st.markdown(f"**{SEVERITY_ICON[rule.severity]} {rule.conclusion}** · {rule.severity} severity")
                    st.write(f"🛠 **Fix:** {rule.advice}")
                    with st.expander("Why? (reasoning trace)"):
                        st.code(engine.explain(rule), language=None)
        else:
            st.caption("No confirmed diagnosis yet.")

        partial = engine.partial_matches(memory, ss.no)
        if partial:
            st.subheader("Possible causes")
            for rule, matched, missing, ratio in partial[:4]:
                st.progress(ratio, text=f"{rule.conclusion} ({len(matched)}/{len(rule.conditions)} signs)")

        asked = ss.yes | ss.no
        question, why_rule = engine.next_question(memory, ss.no, asked)
        if question:
            st.subheader("Follow-up question")
            st.write(f"**{question}?**")
            st.caption(f"Helps confirm: {why_rule.conclusion}")
            c1, c2 = st.columns(2)
            if c1.button("Yes", width="stretch"):
                ss.yes.add(question)
                st.rerun()
            if c2.button("No", width="stretch"):
                ss.no.add(question)
                st.rerun()

# ---------- Knowledge base tab ----------
with tab_kb:
    st.write("All rules in the knowledge base (a condition starting with **@** is a diagnosis reached by another rule).")
    cat = st.selectbox("Category", ["All"] + sorted({r.category for r in RULES}))
    rows = [{"Rule": r.id, "Category": r.category,
             "IF": " AND ".join(r.conditions), "THEN": r.conclusion,
             "Severity": r.severity, "Advice": r.advice}
            for r in RULES if cat in ("All", r.category)]
    st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)
    with st.expander(f"All {len(ASSERTIONS)} assertions"):
        st.dataframe(pd.DataFrame(sorted(ASSERTIONS.items()), columns=["ID", "Assertion"]),
                     width="stretch", hide_index=True)

# ---------- About tab ----------
with tab_about:
    st.markdown("""
**Architecture**
- **Knowledge base** (`knowledge_base.py`): 100 IF-THEN rules, 300 assertions (200 symptoms, 100 diagnoses).
- **Inference engine** (`inference_engine.py`): forward chaining with rule chaining, partial-match ranking, follow-up questions and rule explanations.
- **Natural-language interface** (`nlp.py` + chat UI): maps free text to symptoms using stemming, aliases and weighted word matching.

**Disclaimer:** This is an educational prototype. Always consult a qualified mechanic for safety-critical problems.
""")
