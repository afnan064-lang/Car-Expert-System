"""Lightweight natural-language interface: maps free text to known symptoms.
No external NLP libraries needed (keeps the Streamlit deployment simple)."""
import re
from collections import Counter
from knowledge_base import SYMPTOMS

STOP = {"a", "an", "the", "is", "are", "was", "were", "of", "to", "in", "on", "at", "and", "or",
        "my", "i", "it", "its", "me", "has", "have", "had", "from", "when", "while", "with", "for",
        "does", "do", "did", "been", "be", "that", "this", "there", "very", "really", "some", "after"}

# Free-text phrases -> wording used in the knowledge base
ALIASES = {
    "wont start": "engine does not crank",
    "will not start": "engine does not crank",
    "not starting": "engine does not crank",
    "no start": "engine does not crank",
    "cranks but": "engine cranks but does not start",
    "overheat": "temperature gauge is in the red zone engine overheats",
    "overheating": "temperature gauge is in the red zone engine overheats",
    "running hot": "temperature gauge is in the red zone",
    "flat tire": "tire looks flat",
    "flat tyre": "tire looks flat",
    "tyre": "tire",
    "tyres": "tires",
    "petrol": "fuel",
    "gasoline": "fuel",
    "squeak": "squealing", "squeaking": "squealing", "screech": "squealing", "screeching": "squealing",
    "judder": "vibrates", "shudder": "vibrates", "shaking": "shakes", "vibration": "vibrates",
    "stalls": "stalls", "dies": "stalls", "cuts out": "stalls",
    "a c": "ac", "air conditioner": "ac", "air conditioning": "ac", "aircon": "ac",
    "warm air": "ac blows warm air", "not cold": "ac blows warm air",
    "check engine": "check engine light",
    "mpg": "fuel economy", "mileage": "fuel economy", "uses more fuel": "poor fuel economy",
    "burning rubber": "burning smell", "smells burnt": "burning smell",
    "sputter": "sputters", "knock": "knocking", "ping": "pings", "pinging": "pings",
    "juddering": "vibrates", "wobbling": "wobble", "leak": "leaking", "leaks": "leaking",
    "puddle": "puddle", "smoke": "smoke",
}
NEGATIONS = [("won't", "will not"), ("don't", "do not"), ("doesn't", "does not"),
             ("can't", "cannot"), ("isn't", "is not"), ("didn't", "did not"), ("n't", " not")]


def _stem(w):
    for suf in ("ing", "ed", "es", "s"):
        if w.endswith(suf) and len(w) - len(suf) >= 3:
            return w[: -len(suf)]
    return w


def _tokens(text):
    text = text.lower().replace("’", "'")
    for a, b in NEGATIONS:
        text = text.replace(a, b)
    text = re.sub(r"[^a-z0-9\s-]", " ", text).replace("-", " ")
    text = " " + re.sub(r"\s+", " ", text) + " "
    for k, v in sorted(ALIASES.items(), key=lambda kv: -len(kv[0])):
        text = text.replace(f" {k} ", f" {k} {v} ")
    return {_stem(w) for w in text.split() if w not in STOP}


_SYM_TOKENS = {s: _tokens(s) for s in SYMPTOMS}
_DF = Counter(t for toks in _SYM_TOKENS.values() for t in toks)
_W = {t: 1.0 / n for t, n in _DF.items()}  # rare words matter more


def extract_symptoms(text, threshold=0.6):
    """Return the list of known symptoms that the user's sentence matches."""
    user = _tokens(text)
    found = []
    for sym, toks in _SYM_TOKENS.items():
        hit = toks & user
        if not hit:
            continue
        score = sum(_W[t] for t in hit) / sum(_W[t] for t in toks)
        if score >= threshold and len(hit) >= min(2, len(toks)):
            found.append((score, sym))
    found.sort(reverse=True)
    return [s for _, s in found]
