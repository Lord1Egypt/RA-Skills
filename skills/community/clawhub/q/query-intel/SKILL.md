---
name: query-intel
description: Query rewriting + retrieval gating + outline-first synthesis. Use when a question needs decomposition (Step-Back/Least-to-Most), retrieve-or-skip decisions (CRAG/Self-RAG gates), or multi-source reports (STORM outline-first). Feeds breakthrough-finder stages plan/expand/synthesize.
version: 1.0.0
metadata:
  openclaw:
    requires:
      anyBins: [python3]
---

# Query Intel

Question → better questions → gated retrieval → outline → cited report.

## Commands (`intel.py`, stdlib)

```
python intel.py stepback "<question>"     # principle + sub-questions
python intel.py decompose "<question>"    # least-to-most ordered steps
python intel.py gate "<query>" --conf X   # retrieve|skip + reason
python intel.py outline "<topic>" --slots # outline w/ breakthrough slots
```

## Rules

- Rewriters are retriever-specific: lexical expansion → BM25,
  hypothetical-doc → dense. One universal rewriter fails (RL-QR).
- Skip retrieval when confident AND answer is stable knowledge
  (Self-RAG/FLARE gate) — cuts poisoned/noisy exposure.
- Outline-first always for reports: contradiction / vacancy /
  method-transfer / hostile-evidence slots before any prose.
