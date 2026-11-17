# Troubleshooting (RAGFlow v0.27.3)

- `system-health` fails: Check `RAGFLOW_URL` and inspect the structured response with `--json`; use `list-datasets --page-size 1 --json` to test authentication separately
- `Unknown option for <command>: --...`: Run `node scripts/ragflow.js --help` and use the documented kebab-case option
- "Model not authorized": Verify the model name, factory suffix, and tenant model settings; use a configured model from `list-models`
- "Embedding model identifier must follow `<model_name>@<provider>` format": Use a full identifier from `list-models`, for example `text-embedding-v4@Tongyi-Qianwen`
- `AttributeError("'int' object has no attribute 'split'")` from `create-chat`: Use `<model_name>@<provider>`, for example `qwen-turbo@Tongyi-Qianwen`, not the numeric `id` field
- "Malformed JSON syntax": Fix the JSON payload or file contents before retrying
- Uploaded document name looks like a task ID: Use `--files <original-name>=<path>`; API users can pass `{ path, name }`
- "Can't stop parsing": Only running documents can be stopped
- "No DSL data in request": Pass `--dsl` with a valid JSON object
- "Invalid DSL JSON string.": Pass a JSON object or `@file.json` that can be normalized by the agent parser
- `KeyError('path')` from `create-agent-session`: Include top-level `history`, `path`, `retrieval`, `variables`, `globals`, and `graph`, and make sure every component-backed graph node has `data.name`; see `AGENT_GUIDE.md`
- Iteration agent creates successfully but fails at execution time: Make the upstream `Agent` emit an object with an `items` array and point `Iteration.params.items_ref` at `agent:0@structured.items`; start from `references/examples/agents/04-iteration-agent.json`
- "Dataset doesn't own parsed file": Upload files and start parsing before creating a chat assistant
- "Chunk not found": Verify the chunk ID with `list-chunks` before `update-chunk` or `delete-chunks`
- `rm_chunk deleted chunks 0, expect 1`: `delete-chunks` retries only after exact ID lookup confirms the chunk exists; with `--json`, consume `existing_chunk_ids` and `missing_chunk_ids`; tune with `RAGFLOW_DELETE_CHUNK_RETRIES` and `RAGFLOW_DELETE_CHUNK_RETRY_DELAY_MS`, or run `node scripts/repro-delete-chunks.js --confirm-destructive` for a clean diagnosis
- "`content` is required": Provide non-empty content; omitting `--content` on the CLI keeps the existing chunk text
- `chat-session` returns Not Found: Use the current CLI or client, which posts to `/api/v1/chat/completions` with `chat_id` and `session_id` in the body
- `embed-code` or `embed-chat` returns Unauthorized: Let the CLI auto-create/reuse a token, or pass a valid `--beta` from `/api/v1/system/tokens`
- `embed-code` creates a new token unexpectedly: This matches RAGFlow's embed UI behavior; use `list-system-tokens` to inspect current tokens
- `embed-chat` returns only the prologue or an empty answer: Use the CLI `embed-chat` command, which bootstraps `session_id` automatically, or call `ensureEmbeddedChatSession()` before `embeddedChat()` in API code
- `list-models` returns Unauthorized: Verify `RAGFLOW_API_KEY` is valid and has not expired
- `update-document` gets Method Not Allowed: Use a v0.27.3-compatible server; document updates are sent with `PATCH`
- A list command fails with a `page_size` error: The CLI clamps `--page-size` to 100 and warns; lower the value or page through results
- `Invalid URL`: Use a server root such as `http://localhost:9380`; bare hosts like `localhost:9380` are normalized to `http://...`
- Connection refused: Verify the URL and that the RAGFlow server is running
- API key exposed in logs or chat: Never share keys in chat; regenerate leaked keys and prefer `RAGFLOW_PROVIDER_API_KEY` or `--api-key-file` for provider credentials
- Security warning on ClawHub install: Use a dedicated, rotatable tenant API key, HTTPS in production, and review the disclosed administrative scope
- "Connector authentication failed": Verify the API key, secret, and base URL in the connector configuration
- "Invalid tag format": Use simple strings or arrays of strings for document tags

In `--json` mode, command failures are emitted on stdout as `{ "error": { "message", "raw_message", "code", "status", "command" } }` and exit non-zero. `delete-chunks` may also include `existing_chunk_ids`, `missing_chunk_ids`, `retry_count`, `retries`, and `delete_chunk_diagnostics`.

## v0.27.3 retrieval and parser changes

- If retrieval rejects `rerank_candidates_count`, set `--rerank-candidates-count` to at least `--page × --top-n`. Without flags the server uses page 1, page size 30, and 64 candidates; page 3 at size 30 needs at least 90 candidates.
- If `knn_num_candidates` is rejected, make it at least `knn_top_k` (1024 by default). Prefer `--knn-top-k` over deprecated `--top-k`.
- Connector creation requires `name`, `source`, and `config`; `type` is not a substitute for `source`.
- Dataset/document responses omit legacy `parser_config.graphrag` and `parser_config.raptor` entries. Missing keys do not prove that an indexing task failed; inspect `trace-graphrag` / `trace-raptor` and graph output.
- Document structure graphs now include total and returned entity/relation counts. A limited or filtered graph can return fewer nodes than the totals.

## Stable-release behavior

- An empty retrieval metadata condition skips metadata filtering; an actual condition still intersects with explicit document IDs. There is no filter-only retrieval fallback for unrelated questions.
- Use thumbnail URLs returned by document listings (`/api/v1/documents/{doc_id}/thumbnail`). Document-scoped images use `/api/v1/documents/{doc_id}/images/{image_id}` with authenticated document access; do not reconstruct storage URLs.
- A `CONFIRMATION_REQUIRED` response from parsing is expected: both start and stop clear existing chunks. Verify the target and authorization before adding `--confirm-destructive`.
- Chunk image modes are `append`, `replace`, and `remove`; only append/replace accept image data. Availability must be 0/1 or a boolean in API payloads.
