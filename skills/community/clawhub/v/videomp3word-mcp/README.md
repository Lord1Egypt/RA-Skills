# videomp3word-mcp

`videomp3word-mcp` is a production-oriented MCP and HTTP server that turns unstructured audio/video into structured, monetizable knowledge artifacts through one API.

## What Changed

The previous flat tool proxy has been replaced with a task-oriented knowledge engine:

- one high-level REST endpoint: `POST /video_to_knowledge`
- one primary MCP tool: `video_to_knowledge`
- structured JSON outputs instead of free text
- persistent resources for `MediaAsset`, `Transcript`, `SemanticChunk`, and `KnowledgeUnit`
- DAG workflow execution with retries, checkpoints, and step traces
- modular agents for planning, transcription, semantics, knowledge generation, and evaluation
- export formats for `json`, `markdown`, and Notion-ready blocks
- minimal browser UI at `/`

## Architecture

```text
src/
  agents/        planner, transcription, semantic, knowledge, evaluation
  platform/      orchestration container + video-to-knowledge service
  services/      upstream transcription, model client, exporters
  storage/       repository abstraction + memory/mongodb implementations
  workflow/      DAG executor and workflow types
  ui/            minimal browser playground
  utils/         hashing, safe URL validation, text utilities
  schemas.ts     request/response schemas
  httpServer.ts  REST + MCP-over-HTTP adapter
  mcpServer.ts   MCP stdio/http registration
  index.ts       server bootstrap
```

## Core Endpoint

### `POST /video_to_knowledge`

Request:

```json
{
  "media_url": "https://example.com/demo.mp4",
  "outputs": ["summary", "qa", "flashcards", "tasks", "topics"],
  "mode": "balanced",
  "export_formats": ["json", "markdown", "notion"]
}
```

Response fields:

- `summary`
- `topics`
- `key_points`
- `action_items`
- `qa_pairs`
- `flashcards`
- `entities`
- `confidence_scores`
- `trace`
- `exports`

Sample output: `examples/sample_output.json`

## MCP Surface

- `video_to_knowledge`: primary task tool for ClawHub/OpenClaw style clients
- `videomp3word://knowledge-schema`: resource describing the contract and modes

The package still supports both transports:

- HTTP streamable MCP at `POST /mcp`
- stdio via `npx videomp3word-mcp stdio`

## Modes

- `fast`: lowest cost, larger chunks, shallower reasoning
- `balanced`: default production mode
- `high_accuracy`: smaller chunks, deeper extraction, richer outputs

Mode controls:

- chunk size
- output depth
- model labels in the trace
- transcription settings used for the upstream media call

## Persistence Layer

Collections and indexes:

- `media_assets`: unique index on `normalizedSourceUrl`
- `transcripts`: unique index on `mediaAssetId + transcriptionFingerprint`
- `semantic_chunks`: unique index on `transcriptId + chunkConfigHash + index`
- `knowledge_units`: unique index on `transcriptId + requestHash`
- `workflow_runs`: indexed by `requestHash + createdAt`

If `MONGO_URI` is not configured, the server uses an in-memory repository for local development and smoke tests.

## Environment

Required:

- `VIDEOMP3WORD_SESSION_COOKIE`: upstream videomp3word session used for transcription. Use a dedicated upstream account and inject this at runtime only; never commit it into the package or a checked-in `.env` file.

Recommended:

- `MCP_ACCESS_KEYS`: bearer keys for the REST endpoint and MCP tool
- `MONGO_URI`: MongoDB connection string for persistent storage
- `KNOWLEDGE_MODEL_API_KEY`: explicit API key for the structured knowledge model
- `DASHSCOPE_API_KEY`: fallback key for the original videomp3word DashScope-backed knowledge flow when `KNOWLEDGE_MODEL_API_KEY` is unset
- `KNOWLEDGE_MODEL_API_BASE`: OpenAI-compatible model endpoint, defaults to `https://dashscope.aliyuncs.com/compatible-mode/v1` to match the original videomp3word deployment
- `KNOWLEDGE_MODEL_NAME`: knowledge model name, default `qwen-plus`
- `PUBLIC_BASE_URL`: public base URL of this deployment

## Install And Run

This package ships runnable code, but deployment remains manual: install dependencies, build the TypeScript sources, and then start the server yourself.

```bash
npm install
npm run build
npm start
```

Security notes:

- `VIDEOMP3WORD_BASE_URL` and `KNOWLEDGE_MODEL_API_BASE` must use `https` for non-local deployments so credential-bearing requests are not sent over cleartext HTTP.
- Transcript text, chunk context, and media URLs are sent to the configured upstream transcription service and, when enabled, to the configured knowledge model endpoint. Audit and trust those endpoints before deployment.
- `MCP_ACCESS_KEYS` should be configured before exposing the HTTP or MCP endpoints outside a trusted network.

Local endpoints:

- `GET /health`
- `GET /docs`
- `GET /`
- `POST /video_to_knowledge`
- `POST /mcp`

## Python SDK

Wrapper module: `sdk/python/videomp3word_client.py`

Example:

```python
from sdk.python.videomp3word_client import Videomp3wordClient

client = Videomp3wordClient(base_url="http://localhost:3000", bearer_token="your-access-key")
result = client.video_to_knowledge(
    media_url="https://example.com/demo.mp4",
    outputs=["summary", "qa", "flashcards", "tasks", "topics"],
    mode="balanced",
)
print(result["summary"])
```

## Example Scripts

- `examples/video_to_blog_post.py`
- `examples/meeting_to_action_items.py`
- `examples/podcast_to_summary.py`

## Commercial Positioning

This server is designed as a structured knowledge extraction engine rather than a thin media utility wrapper. That makes it more suitable for SaaS monetization because one call can produce:

- summary content for blogs and newsletters
- Q&A assets for search and support experiences
- flashcards for education products
- action items for meetings and internal productivity workflows
- traceable, exportable JSON for downstream automation

## Verification

```bash
npm run build
npm run smoke
```
