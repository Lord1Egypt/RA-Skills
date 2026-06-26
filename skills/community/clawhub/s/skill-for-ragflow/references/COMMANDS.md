# Command Reference

Full CLI reference for `scripts/ragflow.js`, organized by workflow scenario rather than resource type.

Use `--json` on any command to suppress status text and print only machine-readable JSON.
JSON-valued options such as `--parser-config`, `--prompt-config`, and `--dsl` accept either inline JSON or `@path/to/file.json`.

On command failure with `--json`, the CLI exits non-zero and prints a structured error envelope:

```json
{
  "error": {
    "message": "API Error: Unauthorized",
    "raw_message": "Unauthorized",
    "code": 401,
    "status": 401,
    "command": "list-models"
  }
}
```

## Table of Contents

- [Scenario Map](#scenario-map)
- [Knowledge Base Setup](#knowledge-base-setup)
- [Document Ingestion](#document-ingestion)
- [Parsing and Chunking](#parsing-and-chunking)
- [Information Retrieval](#information-retrieval)
- [RAG Assistant Operation](#rag-assistant-operation)
- [Agent Operation](#agent-operation)
- [Embedded Website Access](#embedded-website-access)
- [Discovery and Configuration](#discovery-and-configuration)
- [System Operations](#system-operations)

## Scenario Map

| Scenario | Use it for |
|---|---|
| [Knowledge Base Setup](#knowledge-base-setup) | Create and maintain datasets before ingesting files |
| [Document Ingestion](#document-ingestion) | Upload, inspect, update, and remove source documents |
| [Parsing and Chunking](#parsing-and-chunking) | Turn documents into searchable chunks and manage chunk content |
| [Information Retrieval](#information-retrieval) | Query datasets directly without creating a chat assistant |
| [RAG Assistant Operation](#rag-assistant-operation) | Create chat assistants, manage sessions, and run Q&A |
| [Agent Operation](#agent-operation) | Create tool-capable agents, manage sessions, and run agent chat |
| [Embedded Website Access](#embedded-website-access) | Generate iframe/widget code and call shared chatbots/agentbots |
| [Discovery and Configuration](#discovery-and-configuration) | Inspect available LLM models, and manage model providers/instances (v0.26.0) |
| [System Operations](#system-operations) | Read version and log-level settings |

## Knowledge Base Setup

Use this section when the user is creating or maintaining the dataset container that everything else depends on.

```bash
node {baseDir}/scripts/ragflow.js create-dataset --name "Tech Docs" --chunk-method naive
node {baseDir}/scripts/ragflow.js create-dataset --name "Tech Docs" --embedding-model "text-embedding-v4@Tongyi-Qianwen"
node {baseDir}/scripts/ragflow.js list-datasets
node {baseDir}/scripts/ragflow.js get-dataset --id <id>
node {baseDir}/scripts/ragflow.js update-dataset --id <id> --name "New Name"
node {baseDir}/scripts/ragflow.js delete-datasets --ids <id1> <id2>
```

When you provide `--embedding-model` to a real v0.26.0 server, use the tenant model identifier format `<model_name>@<provider>`, for example `text-embedding-v4@Tongyi-Qianwen`. Use `list-models` to discover available model/provider pairs.

Typical flow:

1. `create-dataset`
2. `list-datasets` or `get-dataset`
3. `update-dataset` if metadata or chunk method needs adjustment
4. `delete-datasets` only after explicit confirmation

### `list-connectors`

List connectors for a dataset.

**Options**: `--dataset`, `--page`, `--pageSize`, `--json`

### `create-connector`

Create a connector.

**Options**: `--dataset`, `--config` (JSON file), `--json`

**Example**: `node ragflow.js create-connector --dataset <id> --config @connector.json --json`

The connector `--config` is passed through verbatim, so new v0.26.0 connector types work without a CLI change. v0.26.0 adds connectors for OneDrive, Outlook, Microsoft Teams, Slack, SharePoint, Salesforce, and Azure Blob Storage, alongside the existing types (e.g. GitHub). Set the type and auth fields inside the config JSON.

### `get-connector`, `update-connector`, `delete-connector`

Standard CRUD operations.

**Options**: `--id`, `--config` (for update), `--json`
## Document Ingestion

Use this section when the user needs to get files into a dataset or inspect document-level metadata.

```bash
node {baseDir}/scripts/ragflow.js upload-documents --dataset <id> --files ./doc1.pdf ./doc2.txt
node {baseDir}/scripts/ragflow.js upload-documents --dataset <id> --files report.pdf=./tmp/task-output
node {baseDir}/scripts/ragflow.js list-documents --dataset <id> --metadata-condition @metadata_condition.json
node {baseDir}/scripts/ragflow.js get-document --dataset <id> --id <doc_id>
node {baseDir}/scripts/ragflow.js update-document --dataset <id> --id <doc_id> --name "New Name"
node {baseDir}/scripts/ragflow.js update-document --dataset <id> --id <doc_id> --parser-config @parser_config.json --meta-fields @meta_fields.json
node {baseDir}/scripts/ragflow.js metadata-summary --dataset <id> --doc-ids <doc_id1> <doc_id2>
node {baseDir}/scripts/ragflow.js delete-documents --dataset <id> --ids <doc_id1>
node {baseDir}/scripts/ragflow.js download-document --dataset <id> --id <doc_id>
node {baseDir}/scripts/ragflow.js preview-document --id <doc_id>
```

`update-document` follows the current v0.26.0 RAGFlow route and sends `PATCH /api/v1/datasets/{dataset_id}/documents/{document_id}`. It accepts `name`, `parser_config`, `chunk_method`, `enabled`, and `meta_fields`.

`list-documents` supports `metadata`, `metadata_condition`, `return_empty_metadata`, `orderby`, `desc`, `suffix`, `types`, and `run`.

When the physical file path is a temporary or task-generated path, use `--files <original-name>=<path>` so RAGFlow stores the user-facing filename.

Use this when you need to:

- upload raw source files
- inspect a document before parsing
- rename or adjust a document record
- delete a document by explicit ID

## Parsing and Chunking

Use this section after document upload, or when the user wants to control chunk generation directly.

### Parsing workflow

```bash
node {baseDir}/scripts/ragflow.js start-parsing --dataset <id> --doc-ids <doc_id1>
node {baseDir}/scripts/ragflow.js stop-parsing --dataset <id> --doc-ids <doc_id1>
node {baseDir}/scripts/ragflow.js wait-parsing --dataset <id> --doc-ids <doc_id1> --timeout 120
```

Parsing status is observable through `list-documents` by inspecting the `run` field: `UNSTART`, `RUNNING`, `CANCEL`, `DONE`, `FAIL`.
The `run` filter accepts either numeric values (`0`-`4`) or these text labels.

### Chunk operations

```bash
node {baseDir}/scripts/ragflow.js list-chunks --dataset <id> --document <doc_id>
node {baseDir}/scripts/ragflow.js list-chunks --dataset <id> --document <doc_id> --id <chunk_id>
node {baseDir}/scripts/ragflow.js add-chunk --dataset <id> --document <doc_id> --content "chunk content"
node {baseDir}/scripts/ragflow.js update-chunk --dataset <id> --document <doc_id> --chunk <chunk_id> --content "updated content"
node {baseDir}/scripts/ragflow.js delete-chunks --dataset <id> --document <doc_id> --chunk-ids <id1>
node {baseDir}/scripts/repro-delete-chunks.js
```

`add-chunk` writes directly to the document store and returns the generated chunk ID immediately. On Elasticsearch/OpenSearch-style stores, exact `GET` by ID can see a new chunk before search/delete-by-query can see it because insert uses the store refresh cycle. `delete-chunks` handles this by retrying the transient response `rm_chunk deleted chunks 0, expect N` only after an exact ID lookup confirms the target chunk still exists. Tune this with `RAGFLOW_DELETE_CHUNK_RETRIES` and `RAGFLOW_DELETE_CHUNK_RETRY_DELAY_MS`.

With `--json`, `delete-chunks` returns a structured envelope instead of the bare server result:

```json
{
  "result": {},
  "requested_chunk_ids": ["<chunk_id1>"],
  "existing_chunk_ids": ["<chunk_id1>"],
  "missing_chunk_ids": [],
  "visibility_checked": true,
  "retry_count": 1,
  "retries": [
    {
      "attempt": 0,
      "next_attempt": 2,
      "max_retries": 3,
      "existing_chunk_ids": ["<chunk_id1>"],
      "missing_chunk_ids": []
    }
  ]
}
```

If exact-ID checks prove that a target chunk is missing, the command exits non-zero and emits JSON containing `error`, `requested_chunk_ids`, `existing_chunk_ids`, `missing_chunk_ids`, `retry_count`, `retries`, and `delete_chunk_diagnostics`.

If a real server still returns `rm_chunk deleted chunks 0, expect 1` after retries, run `scripts/repro-delete-chunks.js`. The repro creates temporary resources, tries immediate deletion and retry/backoff without the client-side retry wrapper, prints a JSON diagnosis, and removes its dataset.

### Chunk methods

| Method | Use Case |
|--------|----------|
| `naive` | General chunking (default) |
| `manual` | Manual documents |
| `qna` | Q&A pairs |
| `table` | Table data |
| `paper` | Academic papers |
| `book` | Books |
| `laws` | Legal documents |
| `presentation` | Presentations |
| `picture` | Image OCR |
| `one` | Whole document as one chunk |

### `run-raptor`

Start RAPTOR processing for a dataset.

**Options**: `--dataset`, `--json`

### `trace-raptor`

Check RAPTOR processing status.

**Options**: `--dataset`, `--json`
## Information Retrieval

Use this section when the user wants retrieval results directly instead of creating a chat assistant or agent.

```bash
# Basic retrieval
node {baseDir}/scripts/ragflow.js retrieve --question "What is RAG?" --datasets <id>

# Advanced retrieval with keyword + knowledge graph
node {baseDir}/scripts/ragflow.js retrieve \
  --question "machine learning algorithms" \
  --datasets <id1> <id2> \
  --similarity 0.3 \
  --top-n 10 \
  --rerank <rerank_model_id> \
  --keyword \
  --kg
```

### Retrieval parameters

| Parameter | Short | Default | Description |
|-----------|-------|---------|-------------|
| `--question` | `-q` | - | Search question (required) |
| `--datasets` | `-d` | - | Dataset IDs |
| `--similarity` | `-s` | 0.2 | Similarity threshold (0-1) |
| `--top-n` | `-n` | 5 | Number of retrieved chunks; sent as RAGFlow `page_size` |
| `--top-k` | `-k` | 1024 | Number of candidates |
| `--vector-weight` | `-w` | 0.3 | Vector similarity weight (0-1) |
| `--rerank` | `-r` | - | Rerank model ID |
| `--keyword` | | false | Enable keyword search |
| `--kg` | | false | Enable knowledge graph; sent as RAGFlow `use_kg` |
| `--cross-langs` | | - | Cross-language targets |

## RAG Assistant Operation

Use this section when the user wants a dataset-backed chat assistant with reusable sessions.

### Assistant lifecycle

```bash
node {baseDir}/scripts/ragflow.js list-chats
node {baseDir}/scripts/ragflow.js create-chat --name "Tech Q&A" --datasets <id1> <id2> --llm-id qwen-turbo@Tongyi-Qianwen
node {baseDir}/scripts/ragflow.js get-chat --id <chat_id>
node {baseDir}/scripts/ragflow.js update-chat --id <chat_id> --name "New Name"
node {baseDir}/scripts/ragflow.js update-chat --id <chat_id> --prompt-config @prompt_config.json
node {baseDir}/scripts/ragflow.js patch-chat --id <chat_id> --prompt "Use the dataset"
node {baseDir}/scripts/ragflow.js delete-chats --ids <id1> <id2>
```

Use the tenant model identifier format `<model_name>@<provider>` for `--llm-id`. Some deployments return numeric model row IDs from `/v1/llm/my_llms`; do not pass those numeric IDs to `create-chat`.

### Session management

```bash
node {baseDir}/scripts/ragflow.js list-sessions --chat <chat_id>
node {baseDir}/scripts/ragflow.js create-session --chat <chat_id> --name "New Session"
node {baseDir}/scripts/ragflow.js delete-sessions --chat <chat_id> --ids <session_id1>
```

### Ask the assistant

```bash
node {baseDir}/scripts/ragflow.js chat --chat <chat_id> --session <session_id> --question "Hello"
node {baseDir}/scripts/ragflow.js chat-session --chat <chat_id> --session <session_id> --messages @session_messages.json
node {baseDir}/scripts/ragflow.js chat-session --chat <chat_id> --session <session_id> --question "Hello"
```

`chat-session` uses `POST /api/v1/chat/completions` with `chat_id` and `session_id` in the body. When `--messages` is provided, the CLI extracts the last `role: "user"` message as `question`; use `--question` when you already have a single user prompt.

`--pass-all-history` sets `pass_all_history_messages: true`, which replaces the entire stored history with the submitted messages array instead of appending only the latest message (the default behavior in v0.26.0).

Use this path when the user wants multi-turn Q&A over documents without building a full agent workflow.

## Agent Operation

Use this section when the user wants a more autonomous workflow built around an agent DSL and agent sessions.

For a practical guide to the current canvas schema, variable rules, webhook mode, and minimal working DSL files, read [AGENT_GUIDE.md](AGENT_GUIDE.md).

### Agent lifecycle

```bash
node {baseDir}/scripts/ragflow.js list-agents
node {baseDir}/scripts/ragflow.js create-agent --title "Assistant" --dsl '<dsl_json>'
node {baseDir}/scripts/ragflow.js create-agent --title "Assistant" --dsl @agent_dsl.json
node {baseDir}/scripts/ragflow.js create-agent --title "Assistant" --dsl @agent_dsl.json --canvas-type ""
node {baseDir}/scripts/ragflow.js get-agent --id <agent_id>
node {baseDir}/scripts/ragflow.js update-agent --id <agent_id> --title "New Name"
node {baseDir}/scripts/ragflow.js update-agent --id <agent_id> --canvas-type "flow"
node {baseDir}/scripts/ragflow.js delete-agents --ids <id1> <id2>
```

**Options for `list-agents`**:

| Option | Description |
|---|---|
| `--tags` | Filter agents by tags (comma-separated) |
`agent-chat` uses `POST /api/v1/agents/chat/completions` with `agent_id` in the JSON body.

Agents require a DSL workflow definition. A minimal current-schema DSL:

```json
{
  "components": {
    "begin": {
      "obj": {
        "component_name": "Begin",
        "params": {
          "mode": "conversational",
          "prologue": "Hello"
        }
      },
      "downstream": ["message:0"],
      "upstream": []
    },
    "message:0": {
      "obj": {
        "component_name": "Message",
        "params": {
          "content": ["Hello from RAGFlow"]
        }
      },
      "downstream": [],
      "upstream": ["begin"]
    }
  },
  "history": [],
  "path": [],
  "retrieval": [],
  "variables": {},
  "globals": {
    "sys.query": "",
    "sys.user_id": "",
    "sys.conversation_turns": 0,
    "sys.files": [],
    "sys.history": [],
    "sys.date": ""
  },
  "graph": {
    "edges": [],
    "nodes": [
      {
        "id": "begin",
        "type": "beginNode",
        "position": { "x": 50, "y": 200 },
        "data": {
          "label": "Begin",
          "name": "begin",
          "form": {
            "mode": "conversational",
            "prologue": "Hello"
          }
        }
      },
      {
        "id": "message:0",
        "type": "messageNode",
        "position": { "x": 320, "y": 200 },
        "data": {
          "label": "Message",
          "name": "message_0",
          "form": {
            "content": ["Hello from RAGFlow"]
          }
        }
      }
    ]
  }
}
```

The full practical guide and additional minimal examples live in:

- `references/AGENT_GUIDE.md`
- `references/examples/agents/01-conversational-message.json`
- `references/examples/agents/02-retrieval-message.json`
- `references/examples/agents/03-tool-agent.json`
- `references/examples/agents/04-iteration-agent.json`
- `references/examples/agents/05-webhook-message.json`

For iteration flows, prefer the `04-iteration-agent.json` pattern where an upstream `Agent` emits an object with an `items` array and `Iteration.params.items_ref` points to `agent:0@structured.items`.

### `list-agent-tags`

List all agent tags with usage counts.

**Options**: `--json`

**Example**: `node ragflow.js list-agent-tags --json`

### `update-agent-tags`

Update tags for an agent.

**Options**: `--id`, `--tags` (comma-separated), `--json`

**Example**: `node ragflow.js update-agent-tags --id <agent_id> --tags ml,rag --json`
### Agent session management

```bash
node {baseDir}/scripts/ragflow.js list-agent-sessions --agent <agent_id>
node {baseDir}/scripts/ragflow.js create-agent-session --agent <agent_id>
node {baseDir}/scripts/ragflow.js delete-agent-sessions --agent <agent_id> --ids <session_id1>
```

### Ask the agent

```bash
node {baseDir}/scripts/ragflow.js agent-chat --agent <agent_id> --session <session_id> --question "Hello"
node {baseDir}/scripts/ragflow.js agent-chat --agent <agent_id> --session <session_id> --question "Hello" --stream false
node {baseDir}/scripts/ragflow.js agent-chat --agent <agent_id> --session <session_id> --question "Hello" --chat-template-kwargs '{"temperature": 0.5}'
```

`--stream false` requests the final JSON result directly. The bundled client normalizes current `workflow_finished` envelopes into `{ answer, reference, session_id, id }`.

Use this path when the user explicitly wants an agent workflow instead of a simple retrieval assistant.

## Embedded Website Access

Use this section when the user wants the same website embed behavior as RAGFlow's "Embed into site" UI. These commands use `/api/v1/system/tokens` to obtain a token with `beta`, then call the shared `/api/v1/chatbots/*` or `/api/v1/agentbots/*` routes with `Authorization: Bearer <beta>`.

### Token management

```bash
node {baseDir}/scripts/ragflow.js list-system-tokens
node {baseDir}/scripts/ragflow.js create-system-token
node {baseDir}/scripts/ragflow.js delete-system-token --token-file token.txt
cat token.txt | node {baseDir}/scripts/ragflow.js delete-system-token --token-stdin
```

`delete-system-token` reads the token from stdin or a file so the secret never needs to appear in argv. Prefer `--token-stdin` for ad hoc use and `--token-file` when you already store the token in a local file.

`embed-*` commands accept `--beta <token>` when you already have the embedded auth token. Without `--beta`, the CLI reuses the first system token with `beta`; if none exists, it creates one. Treat both the normal system token and the `beta` value as sensitive.

`RAGFLOW_URL` may be a full origin such as `http://localhost:9380` or a bare host such as `localhost:9380`; the CLI normalizes bare hosts to `http://...` when generating iframe URLs.

For `embed-code`, `--origin` is the public web origin that serves the shared chat or agent page. If `--origin` is omitted, the CLI falls back to `RAGFLOW_URL`. On split deployments where the API base URL and browser-facing web origin differ, pass `--origin` explicitly.

### Generate embed code

```bash
node {baseDir}/scripts/ragflow.js embed-code --chat <chat_id> --type fullscreen
node {baseDir}/scripts/ragflow.js embed-code --agent <agent_id> --type widget --published --streaming --user-id <user_id>
```

Common options:

| Option | Description |
|--------|-------------|
| `--chat` / `--agent` | Target chat assistant or agent. Provide exactly one. |
| `--type` | `fullscreen` or `widget`; defaults to `fullscreen`. |
| `--origin` | Public RAGFlow origin for iframe URLs; defaults to `RAGFLOW_URL`. |
| `--theme` | `light` or `dark` for fullscreen embeds. |
| `--locale` | Locale query parameter. |
| `--hide-avatar` | Adds RAGFlow's `visible_avatar=1` shared-page flag. |
| `--published` | Uses the published agent release when embedding agents. |
| `--streaming` | Enables streaming for widget embeds. |
| `--data` | JSON object appended as `data_<key>=<value>` query parameters. |

When presenting results to the user, do not paste raw `token`, `beta`, `src`, or iframe HTML with `auth=` unless the user explicitly asks for the secret material. Use the raw CLI output for execution, but summarize it for the user.

### Inspect and call embedded bots

```bash
node {baseDir}/scripts/ragflow.js embed-info --chat <chat_id>
node {baseDir}/scripts/ragflow.js embed-info --agent <agent_id>
node {baseDir}/scripts/ragflow.js embed-chat --chat <chat_id> --question "Hello"
node {baseDir}/scripts/ragflow.js embed-chat --chat <chat_id> --question "Hello" --stream false
node {baseDir}/scripts/ragflow.js embed-agent-chat --agent <agent_id> --question "Hello" --inputs @begin_inputs.json
```

`embed-chat` accepts `--session`, `--conversation-id`, `--quote`, `--reasoning`, `--internet`, and `--stream false`. `embed-agent-chat` accepts `--session`, `--inputs`, `--user-id`, `--published`, and `--stream false`.

When `--session` is omitted, `embed-chat` first calls the embedded chatbot route with an empty question to create the embedded session, captures `session_id`, and then sends the real question. This mirrors RAGFlow's shared-site iframe behavior. The first no-session response is only the prologue; call the route with `session_id` when implementing your own client.

`embed-info`, `embed-chat`, and `embed-agent-chat` may internally reuse or create embed auth material when `--beta` is omitted. This is expected CLI behavior for automated workflows; summarize the outcome for the user without echoing the secret values by default.

## Discovery and Configuration

Use this section when the user needs to inspect available models before creating datasets, assistants, or agents.

```bash
node {baseDir}/scripts/ragflow.js list-models
node {baseDir}/scripts/ragflow.js list-models --include-details
node {baseDir}/scripts/ragflow.js list-models --group-by factory
node {baseDir}/scripts/ragflow.js list-models --all
```

This is usually the first stop when the user is troubleshooting model availability or deciding which model to use downstream.

RAGFlow v0.26.0 exposes model discovery at `/v1/llm/my_llms`. Authentication uses `RAGFLOW_API_KEY`.

For create operations, use model names plus provider suffixes such as `qwen-turbo@Tongyi-Qianwen` or `text-embedding-v4@Tongyi-Qianwen`. If `list-models --include-details` shows numeric `id` fields, treat them as server row IDs, not values for `--llm-id` or `--embedding-model`.

### Tenant models (v0.26.0)

These commands use the `/api/v1/models` routes (separate from the legacy `list-models` discovery above).

| Command | Purpose | Options |
|---------|---------|---------|
| `list-added-models` | List the tenant's added models | `--type` (filter), `--json` |
| `list-default-models` | List the tenant's default models | `--json` |
| `set-default-model` | Set or clear the default model for a type | `--model-type` (required), `--model-provider`, `--model-instance`, `--model-name`, `--json` |

`set-default-model` requires `--model-type` (one of `chat`, `embedding`, `rerank`, `asr`, `vision`, `tts`, `ocr`). Provide `--model-provider`, `--model-instance`, and `--model-name` to set a default; omit them to clear it.

### Model providers (v0.26.0)

v0.26.0 adds provider/instance/model management under `/api/v1/providers`. An "instance" holds one set of credentials, and a provider can have multiple instances (multiple API keys).

| Command | Purpose | Options |
|---------|---------|---------|
| `list-providers` | List configured providers, or `--available` system providers | `--available`, `--json` |
| `get-provider` | Get provider details | `--name` (required), `--json` |
| `add-provider` | Add a provider for the tenant | `--name` (required), `--json` |
| `delete-provider` | Remove a provider | `--name` (required), `--json` |
| `list-provider-models` | List a provider's available models | `--name` (required), `--api-key`, `--base-url`, `--json` |
| `list-provider-instances` | List a provider's instances | `--name` (required), `--json` |
| `get-provider-instance` | Get one instance | `--name`, `--instance` (both required), `--json` |
| `create-provider-instance` | Create an instance with credentials | `--name`, `--instance`, `--api-key` (required), `--base-url`, `--region`, `--model-info` (JSON), `--json` |
| `delete-provider-instances` | Remove instances | `--name` (required), `--instances` (multiple, required), `--json` |
| `verify-provider` | Test a connection / API key without persisting | `--name`, `--api-key` (required), `--base-url`, `--region`, `--json` |
| `list-instance-models` | List models on an instance | `--name`, `--instance` (required), `--supported`, `--json` |
| `add-instance-model` | Add a model to an instance | `--name`, `--instance`, `--model-name`, `--model-type` (required), `--max-tokens`, `--extra` (JSON), `--json` |
| `set-model-status` | Enable or disable an instance model | `--name`, `--instance`, `--model-name`, `--status` (required), `--json` |

**Example**: `node ragflow.js create-provider-instance --name OpenAI --instance default --api-key sk-... --json`

Treat `--api-key` values as sensitive. Pass them when needed, but do not echo them back to the user. The skill does not wrap the provider "chat to model" test endpoint (`POST /providers/<name>/instances/<instance>/models/<model_name>`); use `chat-session` or `agent-chat` to exercise a configured model instead.

## System Operations

Use this section when the user needs version or log-level configuration.

```bash
node {baseDir}/scripts/ragflow.js system-version
node {baseDir}/scripts/ragflow.js get-log-levels
node {baseDir}/scripts/ragflow.js set-log-level --pkg-name ragflow --level INFO
```
