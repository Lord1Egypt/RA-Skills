# Qwen API Patterns

## Hosted Base URLs

Use the region that matches the enabled Model Studio deployment mode and API key:

| Region | Base URL |
|--------|----------|
| Mainland China | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| Singapore | `https://dashscope-intl.aliyuncs.com/compatible-mode/v1` |
| United States | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |

Required headers:
- `Authorization: Bearer $DASHSCOPE_API_KEY`
- `Content-Type: application/json`

## Hosted Health Check

```bash
QWEN_BASE_URL="https://dashscope-intl.aliyuncs.com/compatible-mode/v1"

curl -s "${QWEN_BASE_URL}/models" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" | jq '.data | map(.id)[:10]'
```

## Minimal Hosted Chat Completion

```bash
curl -s "${QWEN_BASE_URL}/chat/completions" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MODEL_ID",
    "messages": [
      {"role":"system","content":"Be concise and accurate."},
      {"role":"user","content":"Summarize the release notes in 3 bullets."}
    ],
    "temperature": 0.2
  }' | jq -r '.choices[0].message.content'
```

## Strict JSON Pass

Use a separate normalization pass when the first answer needs reasoning freedom:

```bash
curl -s "${QWEN_BASE_URL}/chat/completions" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MODEL_ID",
    "messages": [
      {"role":"system","content":"Return strict JSON with keys label, confidence, action."},
      {"role":"user","content":"Ticket: Customer cannot log in after password reset."}
    ],
    "temperature": 0
  }' | jq -r '.choices[0].message.content' | jq
```

## Local OpenAI-Compatible Check

Use the same pattern for local servers by swapping base URL and auth handling:

```bash
LOCAL_BASE_URL="http://localhost:11434/v1"

curl -s "${LOCAL_BASE_URL}/models" | jq '.data | map(.id)'
```

Typical local defaults:
- Ollama: `http://localhost:11434/v1`
- SGLang: `http://localhost:30000/v1`
- vLLM: use the port chosen at launch

## Minimal Local Chat Check

```bash
curl -s "${LOCAL_BASE_URL}/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MODEL_ID",
    "messages": [
      {"role":"user","content":"Reply with only the word READY."}
    ],
    "temperature": 0
  }' | jq -r '.choices[0].message.content'
```

## Retry Rules

- Retry `429` and transient `5xx` with capped exponential backoff.
- Do not retry malformed JSON forever; shrink the task or add a second normalization pass.
- If hosted and local routes both exist, keep one fallback route per workload.
