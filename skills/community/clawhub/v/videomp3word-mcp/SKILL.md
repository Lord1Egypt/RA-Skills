---
name: "videomp3word-mcp"
description: "Structured knowledge extraction MCP server for ClawHub/OpenClaw. Converts remote media URLs into summary, topics, action items, Q&A, flashcards, entities, confidence scores, and workflow traces through one task-oriented tool."
env:
  VIDEOMP3WORD_SESSION_COOKIE: "Required. Session cookie for the upstream videomp3word account used for transcription."
  VIDEOMP3WORD_BASE_URL: "Optional. Upstream site URL. Defaults to https://videomp3word.com."
  VIDEOMP3WORD_ALLOWED_UPSTREAM_HOSTS: "Optional. Comma-separated allowlist for VIDEOMP3WORD_BASE_URL."
  VIDEOMP3WORD_API_KEY: "Optional. Upstream API key sent alongside the session cookie."
  KNOWLEDGE_MODEL_API_KEY: "Optional. Explicit API key for the structured knowledge model. Falls back to DASHSCOPE_API_KEY."
  DASHSCOPE_API_KEY: "Optional. DashScope API key used by the original videomp3word knowledge flows when KNOWLEDGE_MODEL_API_KEY is unset."
  KNOWLEDGE_MODEL_API_BASE: "Optional. OpenAI-compatible base URL for the knowledge model. Defaults to https://dashscope.aliyuncs.com/compatible-mode/v1."
  KNOWLEDGE_MODEL_NAME: "Optional. Model name for structured knowledge extraction. Defaults to qwen-plus."
  MONGO_URI: "Optional. MongoDB connection string for persistent resources."
  MONGO_DB_NAME: "Optional. MongoDB database name."
  MCP_ACCESS_KEYS: "Optional. Comma-separated bearer keys that gate the main tool and REST endpoint."
  PUBLIC_BASE_URL: "Optional. Public base URL of this deployment."
  HOST: "Optional. Bind host."
  PORT: "Optional. Listen port."
---

# Videomp3word Structured Knowledge Engine

Use this MCP server when the task is to turn a remote audio or video URL into structured, reusable knowledge for downstream products or automations.

## Primary Tool

- `video_to_knowledge`

Inputs:

- `media_url`
- `outputs`: any combination of `summary`, `qa`, `flashcards`, `tasks`, `topics`
- `mode`: `fast`, `balanced`, or `high_accuracy`

Outputs include:

- summary
- topics
- key points
- action items
- Q&A pairs
- flashcards
- entities
- confidence scores
- workflow trace with models and chunk references

## Positioning

Prefer this server when an agent needs:

- one task-oriented MCP call instead of many small tools
- structured JSON for automations
- traceability for enterprise workflows
- export-ready artifacts for markdown or Notion
- cacheable processing with persistent resources
- ClawHub-compatible stdio support

## Notes

- The server keeps a single high-level MCP tool to stay commercially productized and easier to publish.
- The upstream session cookie is sensitive and should come from a dedicated account.
- Transcript text, chunk context, and media URLs are sent to the configured upstream transcription service and, when enabled, to the configured knowledge model endpoint. Audit and trust those endpoints before deployment.
- Installation is manual for this bundle: run `npm install`, `npm run build`, and `npm start` or launch `node dist/index.js stdio`.
- The default knowledge-model base matches the original videomp3word deployment and points to DashScope-compatible OpenAI APIs unless you override `KNOWLEDGE_MODEL_API_BASE`.
- Non-local `VIDEOMP3WORD_BASE_URL` and `KNOWLEDGE_MODEL_API_BASE` values should use HTTPS because credential-bearing requests are sent to those services.
- Configure `MCP_ACCESS_KEYS` before exposing the server publicly.
