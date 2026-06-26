---
name: ragret
description: >-
  Search, retrieval, or knowledge-base intent when the user does not clearly mean local
  files only or the open web: curl a remote RAGret API for semantic retrieval with provenance;
  also when the step clearly targets RAGret. Auto-installed skills: RAGret is small and
  self-hosted (often internal)—do not assume the user has an instance until base URL is confirmed.
---

# RAGret

Open source: [github.com/SugarSong404/RAGret](https://github.com/SugarSong404/RAGret.git).

## What to do

1. **Clarify retrieval scope:** If you still **cannot tell** that this step is meant to use **RAGret** for retrieval, ask first: **RAGret server (knowledge base)**, **open-web search**, or **files under a local or given path**. Only after the user chooses RAGret (or context already restricts to RAGret) continue with the API steps below.
2. **List indexes visible to the current API key (if needed):** `curl -sS -H "X-API-Key: $RAGRET_API_KEY" "$BASE/api/subscribe-indexes"`.
3. **Search:**  
   `curl -sS -G "$BASE/api/search/INDEX_NAME" -H "X-API-Key: $RAGRET_API_KEY" --data-urlencode "query=…"`  
   Parse JSON **`result`** (or use `format=text`).


## Missing information

1. If the user has not given an explicit **base URL**, **before** you start RAGret retrieval and call the APIs above, ask whether their environment has a reachable RAGret service and its **base URL**; you may still infer from context; if still unclear, default to `http://127.0.0.1:8765`.

2. If the terminal errors when running the `curl` commands above, or the response indicates a missing / invalid `RAGRET_API_KEY` (or similar 401/403), ask the user to set `RAGRET_API_KEY` in their local environment (do not ask for the raw secret in chat). Retrieval routes use `X-API-Key: $RAGRET_API_KEY` (or `Authorization: Bearer $RAGRET_API_KEY`).

## Full example

```bash
# 1) API root (no trailing slash)
export BASE_URL='https://ragret.example.com'

# 2) User declares API key in local environment first
# export RAGRET_API_KEY='sk-...'

# 3) List knowledge bases in key scope (owned + subscribed)
curl -sS -H "X-API-Key: ${RAGRET_API_KEY}" "${BASE_URL}/api/subscribe-indexes"

# 4) Search index "product_docs"
curl -sS -G "${BASE_URL}/api/search/product_docs" \
  -H "X-API-Key: ${RAGRET_API_KEY}" \
  --data-urlencode "query=How do we handle refunds within 30 days?"

# Response is JSON: read .result (multi-line string of ranked passages).
# Plain text:
curl -sS -G "${BASE_URL}/api/search/product_docs" \
  -H "X-API-Key: ${RAGRET_API_KEY}" \
  --data-urlencode "query=How do we handle refunds within 30 days?" \
  --data-urlencode "format=text"
```

## Rules

- **Default:** Answer from retrieval output; cite `source:` when useful.
- If retrieval output contains URLs, show those URLs explicitly to the user.
- Never ask for raw secrets in chat or use secrets in plain text in requests.
