---
name: weryai-chat
description: Chat, ask, compare, and inspect WeryAI chat models through the official OpenAI-compatible chat completions API. Use when you need general assistant chat, multi-turn conversation, chat model lookup, model comparison, prompt-response tasks, or direct message-array calls against WeryAI chat models.
metadata: { "openclaw": { "emoji": "💬", "primaryEnv": "WERYAI_API_KEY", "paid": true, "network_required": true, "requires": { "env": ["WERYAI_API_KEY"], "bins": ["node"], "node": ">=18" } } }
---

# WeryAI Chat

Use the official WeryAI chat-completions API for general assistant chat and model lookup. This skill is intentionally broad but not specialized: it is for general conversation and prompt-response tasks, not blog writing, social copy, or email drafting.

## Example Prompts

- `Ask a WeryAI chat model to explain retrieval augmented generation in plain English.`
- `Send this messages array to WeryAI chat completions and return the assistant response.`
- `List the currently available WeryAI chat models and their pricing.`
- `Use GPT_5_4 for this one chat call instead of the default model.`

## Quick Summary

- Main jobs: `general assistant chat`, `multi-turn chat`, `chat model lookup`, `prompt-response`
- Default model: `GEMINI_3_1_PRO`
- Main optional controls: `model`, `messages`, `maxTokens`, `temperature`, `topP`
- Main trust signals: dry-run support, model lookup, OpenAI-compatible messages, explicit non-specialized scope

## Prerequisites

- `WERYAI_API_KEY` must be set before calling the API.
- Node.js `>=18` is required.
- Real runs use the WeryAI chat completion API and may consume credits.

## When to use this skill

Use this skill when the user wants:

- a normal assistant-style answer
- a direct chat-completions call
- a multi-turn conversation via `messages`
- model lookup or model selection before a chat run

Do not use this skill when the user clearly wants:

- blog writing
- email drafting
- ad copy
- translation or summarization as the main task

Those belong to the existing specialized `text/*` skills.

## OpenAI-compatible message shape

This skill accepts standard chat-completions messages:

```json
[
  { "role": "system", "content": "You are a helpful assistant." },
  { "role": "user", "content": "What is artificial intelligence?" }
]
```

If you provide `messages`, they are passed through directly. If you provide only `prompt`, the runtime builds a simple messages array automatically.

## Commands

```sh
# List available chat models
node {baseDir}/scripts/models.js

# Simple prompt-response chat
node {baseDir}/scripts/write.js --json '{
  "prompt":"Explain retrieval augmented generation in plain English",
  "temperature":0.7
}'

# Explicit messages array
node {baseDir}/scripts/write.js --json '{
  "model":"GPT_5_4",
  "messages":[
    {"role":"system","content":"You are concise and technical."},
    {"role":"user","content":"Compare RAG and long-context prompting."}
  ]
}'

# Dry-run preview
node {baseDir}/scripts/write.js --json '{
  "prompt":"What is the difference between latency and throughput?"
}' --dry-run
```

## Workflow

1. If the user wants model choice or pricing context first, run `models.js`.
2. Use `write.js` for direct prompt-response or explicit `messages` chat.
3. Prefer `--dry-run` when validating payload shape without spending credits.
4. Return the assistant response directly when the call succeeds.

## Definition of Done

- `models.js` returns the available chat models and pricing metadata.
- `write.js` returns at least one assistant completion choice and non-empty text, or a clear API failure.

## Re-run Behavior

- Re-running `models.js` is read-only and safe.
- Re-running `write.js --dry-run` is safe and does not call the API.
- Re-running `write.js` creates a fresh chat completion request and may consume additional credits.

## References

- Official chat API summary: [references/chat-api.md](references/chat-api.md)
- Chat completion API: [Chat Completion](https://docs.weryai.com/api-reference/chat/chat-completion)
- Chat models API: [Get Chat Models List](https://docs.weryai.com/api-reference/chat/get-chat-models-list)
