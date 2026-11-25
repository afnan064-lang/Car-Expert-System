# 🚗 Vehicle Troubleshooting Expert System

Rule-based expert system (Python + Streamlit) that diagnoses common vehicle problems.

| Component | File |
|---|---|
| Knowledge base: 100 rules, 300 assertions | `knowledge_base.py` |
| Inference engine (forward chaining, follow-up questions, explanations) | `inference_engine.py` |
| Natural-language interface | `nlp.py` + chat UI in `app.py` |

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud
1. Push this folder to a GitHub repo.
2. Go to https://share.streamlit.io → **New app** → select the repo, branch `main`, main file `app.py`.
3. Click **Deploy**.

## Test
```bash
pip install pytest && pytest
```
