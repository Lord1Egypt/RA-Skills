# Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| "Model not authorized" | Requested model is not configured for this tenant, or the model/factory name does not match | Verify the model name, factory suffix, and tenant model settings; use a configured model from `list-models` |
| "Embedding model identifier must follow `<model_name>@<provider>` format" | `create-dataset --embedding-model` used only the model name | Use a full identifier from `list-models`, for example `text-embedding-v4@Tongyi-Qianwen` |
| `AttributeError("'int' object has no attribute 'split'")` from `create-chat` | A numeric model row ID from `list-models` was sent as `--llm-id` | Use `<model_name>@<provider>`, for example `qwen-turbo@Tongyi-Qianwen`, not the numeric `id` field |
| "Malformed JSON syntax" | The request body is not valid JSON | Fix the JSON payload or file contents before retrying |
| Uploaded document name looks like a task ID | The physical path passed to `--files` is a temporary/task-generated filename, and RAGFlow stores the multipart `filename` as document name | Use `--files <original-name>=<path>`; API users can pass `{ path, name }` |
| "Can't stop parsing" | The document is already done or has not started yet | Only running documents can be stopped |
| "No DSL data in request" | Agent creation omitted the DSL payload | Pass `--dsl` with a valid JSON object |
| "Invalid DSL JSON string." | The DSL payload is not valid JSON | Pass a JSON object or `@file.json` that can be normalized by the agent parser |
| `KeyError('path')` from `create-agent-session` | Agent DSL is missing runtime fields required by RAGFlow Canvas | Include top-level `history`, `path`, `retrieval`, `variables`, `globals`, and `graph`, and make sure every component-backed graph node has `data.name`; see `AGENT_GUIDE.md` |
| Iteration agent creates successfully but fails at execution time | `items_ref` resolved to a non-list, often because the upstream `Agent` did not produce `structured.items` | Make the upstream `Agent` emit an object with an `items` array and point `Iteration.params.items_ref` at `agent:0@structured.items`; start from `references/examples/agents/04-iteration-agent.json` |
| "Dataset doesn't own parsed file" | The dataset has no parsed documents yet | Upload files and start parsing before creating a chat assistant |
| "Chunk not found" | Chunk ID does not exist or belongs to another document | Verify the chunk ID with `list-chunks` before `update-chunk` or `delete-chunks` |
| `rm_chunk deleted chunks 0, expect 1` | The RAGFlow server accepted the chunk ID but document-store search/delete visibility lagged behind exact ID visibility | `delete-chunks` retries only after exact ID lookup confirms the chunk exists; with `--json`, consume `existing_chunk_ids` and `missing_chunk_ids`; tune with `RAGFLOW_DELETE_CHUNK_RETRIES` and `RAGFLOW_DELETE_CHUNK_RETRY_DELAY_MS`, or run `node scripts/repro-delete-chunks.js` for a clean diagnosis |
| "`content` is required" | Empty content was submitted to chunk update or set | Provide non-empty content; omitting `--content` on the CLI keeps the existing chunk text |
| `chat-session` returns Not Found | You are calling the login-session frontend route instead of the API-key SDK route | Use the current CLI or client, which posts to `/api/v1/chat/completions` with `chat_id` and `session_id` in the body |
| `embed-code` or `embed-chat` returns Unauthorized | The embedded shared-site routes authenticate with the system token `beta`, not `RAGFLOW_API_KEY` | Let the CLI auto-create/reuse a token, or pass a valid `--beta` from `/api/v1/system/tokens` |
| `embed-code` creates a new token unexpectedly | No existing system token had a `beta` value | This matches RAGFlow's embed UI behavior; use `list-system-tokens` to inspect current tokens |
| `embed-chat` returns only the prologue or an empty answer | The embedded chatbot route was called without `session_id`; RAGFlow uses that first call to create the iframe session | Use the CLI `embed-chat` command, which bootstraps `session_id` automatically, or call `ensureEmbeddedChatSession()` before `embeddedChat()` in API code |
| `list-models` returns Unauthorized | The `/v1/llm/my_llms` endpoint rejected the API key | Verify `RAGFLOW_API_KEY` is valid and has not expired |
| `update-document` gets Method Not Allowed | The server does not match the v0.26.0 route shape expected by this skill | Use a v0.26.0-compatible server; document updates are sent with `PATCH` |
| A list command fails with a `page_size` error | RAGFlow v0.26.0 caps `page_size` at 100 on list endpoints | The CLI clamps `--page-size` to 100 and warns; lower the value or page through results |
| `Invalid URL` | `RAGFLOW_URL` is empty or malformed | Use a server root such as `http://localhost:9380`; bare hosts like `localhost:9380` are normalized to `http://...` |
| Connection refused | `RAGFLOW_URL` is wrong or the server is down | Verify the URL and that the RAGFlow server is running |
| API key exposed in logs or chat | The API key was shared or logged | Never share `RAGFLOW_API_KEY` in chat; regenerate the key if leaked |
| Security warning on ClawHub install | The skill requires `RAGFLOW_API_KEY` which grants access to your RAGFlow deployment | Use a least-privilege API key, use HTTPS in production, and review permissions before approving |
| "Connector authentication failed" | The external service rejected the connector credentials or the endpoint is unreachable | Verify the API key, secret, and base URL in the connector configuration |
| "Invalid tag format" | Document tags were submitted in an unsupported format (e.g. nested objects) | Use simple strings or arrays of strings for document tags |

In `--json` mode, command failures are emitted on stdout as `{ "error": { "message", "raw_message", "code", "status", "command" } }` and exit non-zero. `delete-chunks` may also include `existing_chunk_ids`, `missing_chunk_ids`, `retry_count`, `retries`, and `delete_chunk_diagnostics`.