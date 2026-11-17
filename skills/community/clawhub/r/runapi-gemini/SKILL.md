---
name: gemini
description: Call Gemini 2.5 and 3 series models through RunAPI using Gemini contents clients. Use for Gemini chat, streaming, multimodal input, grounding, structured output, reasoning, or an existing compatibility client that needs the conditional reference.
documentation: https://runapi.ai/models/gemini.md
provider_page: https://runapi.ai/providers/google.md
catalog: https://runapi.ai/models.md
metadata:
  openclaw:
    homepage: https://runapi.ai/models/gemini
    primaryEnv: GEMINI_API_KEY
    requires:
      env: [GEMINI_API_KEY, GEMINI_BASE_URL]
    envVars:
    - {name: GEMINI_API_KEY, required: true, description: RunAPI API key used by Gemini contents clients.}
    - {name: GEMINI_BASE_URL, required: true, description: Set to https://runapi.ai for Gemini on RunAPI.}
---

# Gemini on RunAPI

Use Gemini contents at `https://runapi.ai` with `generateContent` or
`streamGenerateContent` as the primary protocol.

## Primary protocol recipe

### Authenticate

Set `GEMINI_API_KEY` to a RunAPI API key and the Gemini client base URL to
`https://runapi.ai`. Raw requests send the key with `x-goog-api-key`.

### Send request

```bash
curl -X POST \
  "https://runapi.ai/v1beta/models/gemini-3.7-flash:streamGenerateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"contents":[{"role":"user","parts":[{"text":"Summarize this review."}]}]}'
```

Use `generateContent` only when the selected model supports synchronous output;
`gemini-3.7-flash` accepts only `streamGenerateContent`. For this model, native
tools are limited to `functionDeclarations` and the `googleSearch` tool with an
empty object payload;
native thinking is limited to `generationConfig.thinkingConfig.includeThoughts`
and `thinkingLevel` of `low` or `high`.

### Verify result

Require candidate content, terminal `finishReason`, and `usageMetadata`. A
stream is complete only after the terminal candidate and Usage; an HTTP 2xx
without both is incomplete.

### Stop boundaries

Correct a rejected shape once using the structured error. Retry transport once
only before any candidate or Usage and when replay is safe. Record a terminal
error and stop without changing model or protocol.

## Compatibility protocols

Load [compatibility protocols](references/compatibility-protocols.md) only when an existing client requires OpenAI-compatible Chat Completions.

## Supported models

| Model ID | Use when |
|---|---|
| `gemini-3.8-flash` | Fast text-only chat and function calling; image, audio, and file input are rejected |
| `gemini-3.7-flash` | Fast streaming chat; use native tools/search grounding only with Gemini contents |
| `gemini-3.6-flash` | Fast current-generation multimodal requests |
| `gemini-3.5-flash` | Fast multimodal and function-calling requests |
| `gemini-3.5-flash-lite` | Lightweight text generation with native Gemini streaming |
| `gemini-3.1-pro-preview` | Complex multimodal and reasoning requests |
| `gemini-3.1-flash-lite` | Lightweight text-only requests; image, audio, and file input are rejected |
| `gemini-3-flash-preview` | Preview flash workloads |
| `gemini-2.5-pro` | Stable high-quality multimodal requests |
| `gemini-2.5-flash` | Stable fast multimodal requests |
| `gemini-2.5-flash-lite` | Lightweight text-only requests; image, audio, and file input are rejected |

## References

- <https://runapi.ai/models/gemini.md>
- <https://runapi.ai/providers/google.md>
- <https://runapi.ai/models.md>
