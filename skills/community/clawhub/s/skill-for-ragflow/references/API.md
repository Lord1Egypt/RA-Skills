# Programmatic API and Configuration

## Table of Contents

- [Setup](#setup)
- [Dataset](#dataset)
- [Document](#document)
- [Document Download](#document-download)
- [Parsing](#parsing)
- [Chunk](#chunk)
- [Retrieval](#retrieval)
- [Connector](#connector)
- [RAPTOR](#raptor)
- [Chat Assistant](#chat-assistant)
- [Session](#session)
- [Chat Conversation](#chat-conversation)
- [Agent](#agent)
- [Agent Tags](#agent-tags)
- [Agent Session](#agent-session)
- [Agent Chat](#agent-chat)
- [Embedded Website Access](#embedded-website-access)
- [LLM Models](#llm-models)
- [System](#system)
- [Utility](#utility)
- [Configuration](#configuration)

## Setup

```javascript
const { createClient } = require("{baseDir}/lib/api.js");
const client = createClient();
```

`createClient()` reads `RAGFLOW_URL` and `RAGFLOW_API_KEY` from the environment and then fills missing values from the bundled `.env` file. Existing environment variables take precedence. See [Configuration](#configuration) below.

## Dataset

```javascript
// List datasets (supports pagination: page, page_size, id, name)
const datasets = await client.listDatasets({ page: 1, page_size: 10 });

// Get a single dataset by ID (enriched with total_size and connectors)
const dataset = await client.getDataset("<dataset_id>");
// Returns: { id: "...", name: "...", total_size: 1024, connectors: [...], ... }

// Create a dataset
const dataset = await client.createDataset({
  name: "Tech Docs",
  chunk_method: "naive",
});

// Update a dataset
await client.updateDataset("<dataset_id>", { name: "New Name" });

// Delete datasets by IDs
await client.deleteDatasets(["<id1>", "<id2>"]);
```

## Document

```javascript
// Upload documents
await client.uploadDocuments("<dataset_id>", ["./report.pdf", "./notes.txt"]);

// Override display names when paths are temporary/task IDs
await client.uploadDocuments("<dataset_id>", [
  { path: "./tmp/task-output", name: "report.pdf" },
]);

// List documents (supports page, page_size, id, name, orderby, desc, keywords, suffix, types, run, metadata, metadata_condition, return_empty_metadata)
const docs = await client.listDocuments("<dataset_id>");

// Get a single document by ID
const doc = await client.getDocument("<dataset_id>", "<doc_id>");

// Update a document
await client.updateDocument("<dataset_id>", "<doc_id>", {
  name: "Renamed",
  parser_config: { pages: [[1, 2]] },
  chunk_method: "knowledge_graph",
  enabled: 1,
  meta_fields: { author: "Alice" },
});

// Delete documents by IDs
await client.deleteDocuments("<dataset_id>", ["<doc_id1>", "<doc_id2>"]);
```

RAGFlow v0.26.0 defines document updates as `PATCH /api/v1/datasets/{dataset_id}/documents/{document_id}`. `updateDocument()` sends that request directly.

You can also filter documents by metadata:

```javascript
const docs = await client.listDocuments("<dataset_id>", {
  metadata_condition: JSON.stringify({
    logic: "and",
    conditions: [{ name: "status", comparison_operator: "=", value: "published" }],
  }),
});
```

You can also summarize metadata across documents:

```javascript
const summary = await client.metadataSummary("<dataset_id>", ["<doc_id1>", "<doc_id2>"]);
// Returns: { summary: [...] }
```

## Document Download

```javascript
// Download via dataset
const doc = await client.downloadDocument(datasetId, documentId);

// Download by document ID
const doc = await client.downloadDocumentById(documentId);

// Preview a document inline (v0.26.0)
const preview = await client.previewDocument(documentId);
```

## Parsing

```javascript
// Start parsing (returns immediately)
await client.startParsing("<dataset_id>", ["<doc_id1>"]);

// Stop parsing
await client.stopParsing("<dataset_id>", ["<doc_id1>"]);

// Wait for parsing to complete (polls until DONE or FAIL)
// Documents stuck in CANCEL keep polling until timeout.
const results = await client.waitForParsing("<dataset_id>", ["<doc_id1>"], {
  interval: 3000,   // poll interval in ms (default: 3000)
  maxWait: 120000,  // max wait in ms (default: 120000)
});
```

## Chunk

```javascript
// List chunks (supports pagination: page, page_size, keywords)
const chunks = await client.listChunks("<dataset_id>", "<doc_id>");

// Exact chunk lookup by ID
const chunk = await client.getChunk("<dataset_id>", "<doc_id>", "<chunk_id>");

// Add a chunk
await client.addChunk("<dataset_id>", "<doc_id>", {
  content: "Custom chunk text",
  important_keywords: ["keyword1", "keyword2"],
});

// Update a chunk
await client.updateChunk("<dataset_id>", "<doc_id>", "<chunk_id>", {
  content: "Updated content",
  important_keywords: ["new_keyword"],
});

// Delete chunks by IDs
await client.deleteChunks("<dataset_id>", "<doc_id>", ["<chunk_id1>"]);
```

`deleteChunks()` retries the transient `rm_chunk deleted chunks 0, expect N` response only after `getChunk()` confirms the target chunk still exists. This distinguishes document-store refresh delay from a genuinely missing chunk. Override with:

```javascript
await client.deleteChunks("<dataset_id>", "<doc_id>", ["<chunk_id1>"], {
  maxRetries: 0,
  retryDelay: 1000,
});
```

When the CLI is run with `--json`, `delete-chunks` wraps the server result with diagnostic fields that pipelines can consume directly:

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

On a final delete visibility failure, the CLI exits non-zero and emits JSON with `error`, `requested_chunk_ids`, `existing_chunk_ids`, `missing_chunk_ids`, `retry_count`, `retries`, and `delete_chunk_diagnostics`.

All CLI command failures in `--json` mode use the same top-level error envelope:

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

Command-specific diagnostics, such as delete chunk visibility checks, are added as extra top-level fields alongside `error`.

## Retrieval

```javascript
const results = await client.retrieve({
  question: "What is deep learning?",
  dataset_ids: ["<dataset_id>"],
  similarity_threshold: 0.3,
  page_size: 5,
  top_k: 1024,
  vector_similarity_weight: 0.7,
  keyword: true,
  use_kg: false,
  rerank_id: "<rerank_model_id>",
});
```

## Connector

```javascript
// List connectors
const connectors = await client.listConnectors(datasetId);

// Create connector
const connector = await client.createConnector(datasetId, {
  name: "REST API",
  type: "rest",
  config: { url: "https://api.example.com" }
});

// Get, update, delete connector
const conn = await client.getConnector(connectorId);
await client.updateConnector(connectorId, { name: "Updated" });
await client.deleteConnector(connectorId);
```

## RAPTOR

```javascript
// Start RAPTOR processing
const task = await client.runRaptor(datasetId);

// Check progress
const progress = await client.traceRaptor(datasetId);
```

## Chat Assistant

```javascript
// List chat assistants (supports pagination)
const chats = await client.listChatAssistants({ page: 1, page_size: 10 });

// Get a single chat assistant by ID
const chat = await client.getChatAssistant("<chat_id>");

// Create a chat assistant
const chat = await client.createChatAssistant({
  name: "Tech Q&A",
  dataset_ids: ["<dataset_id>"],
  llm_id: "qwen-turbo@Tongyi-Qianwen",
  prompt_config: { system: "You are a helpful assistant." },
  similarity_threshold: 0.3,
  top_n: 5,
});

// Update a chat assistant
await client.updateChatAssistant("<chat_id>", { name: "New Name" });

// Patch a chat assistant
await client.patchChatAssistant("<chat_id>", { prompt_config: { system: "Use the dataset" } });

// Delete chat assistants by IDs
await client.deleteChatAssistants(["<chat_id1>", "<chat_id2>"]);
```

## Session

```javascript
// List sessions for a chat assistant
const sessions = await client.listSessions("<chat_id>", { page: 1 });

// Create a session
const session = await client.createSession("<chat_id>", { name: "Q&A Session" });

// Delete sessions by IDs
await client.deleteSessions("<chat_id>", ["<session_id1>"]);
```

## Chat Conversation

```javascript
// Chat with an assistant (streaming SSE, returns final answer + references)
const answer = await client.chat("<chat_id>", "<session_id>", "What is RAG?");
// Returns: { answer: "...", reference: { ... } }

// Chat with a session (messages payload)
const sessionAnswer = await client.chatSession("<chat_id>", "<session_id>", {
  question: "Summarize the policy.",
});

// Convenience form: the last user message becomes `question`
const sessionAnswerFromMessages = await client.chatSession("<chat_id>", "<session_id>", {
  messages: [
    { role: "system", content: "Follow the dataset." },
    { role: "user", content: "Summarize the policy." },
  ],
});
```

`chatSession()` uses `POST /api/v1/chat/completions` with `chat_id` and `session_id` in the JSON body. In v0.26.0, `conversation_id` is accepted as an alias for `session_id`. By default, only the latest user message is appended to the stored history. Set `pass_all_history_messages: true` to replace the entire history with the submitted messages array.

## Agent

```javascript
// List agents (supports pagination)
const agents = await client.listAgents({ page: 1 });

// Get a single agent by ID
const agent = await client.getAgent("<agent_id>");

// Create an agent (use the current canvas DSL schema from AGENT_GUIDE.md)
const agent = await client.createAgent({ title: "My Agent", dsl: { ... } });

// Update an agent
await client.updateAgent("<agent_id>", { title: "Updated Agent" });

// Delete agents by IDs
await client.deleteAgents(["<agent_id1>"]);
```

`createAgent()` and `updateAgent()` forward the DSL directly to RAGFlow, where the server normalizes it through the canvas DSL normalization layer. In practice, hand-authored DSL should include `components`, `history`, `path`, `retrieval`, `variables`, `globals`, and `graph`, and every component-backed graph node should include `data.name`. See [AGENT_GUIDE.md](AGENT_GUIDE.md) for the current schema and minimal examples.

## Agent Tags

```javascript
// List all agent tags
const tags = await client.listAgentTags();

// Update agent tags
await client.updateAgentTags(agentId, ["ml", "rag"]);
```

## Agent Session

```javascript
// List agent sessions
const sessions = await client.listAgentSessions("<agent_id>", { page: 1 });

// Create an agent session
const session = await client.createAgentSession("<agent_id>", { name: "Session 1" });

// Delete agent sessions by IDs
await client.deleteAgentSessions("<agent_id>", ["<session_id1>"]);
```

## Agent Chat

```javascript
// Chat with an agent (streaming SSE, returns final answer + references)
const answer = await client.agentChat("<agent_id>", "<session_id>", "Analyze the data");
// Returns: { answer: "...", reference: { ... } }

// Ask for a final JSON response instead of SSE
const finalAnswer = await client.agentChat("<agent_id>", "<session_id>", "Analyze the data", {
  stream: false,
});
// Returns: { answer: "...", reference: { ... }, session_id: "...", id: "..." }
```

When `stream: false` is used, `agentChat()` still normalizes current `workflow_finished` or `done` JSON envelopes into the same final answer shape used by the streaming path.
`agentChat()` uses `POST /api/v1/agents/chat/completions` with `agent_id` in the JSON body.

## Embedded Website Access

```javascript
// Reuse an existing system token with beta, or create one if needed
const embedToken = await client.ensureEmbedToken();

// Token management
const tokens = await client.listSystemTokens();
const newToken = await client.createSystemToken();
await client.deleteSystemToken(newToken.token);

// Chat assistant shared-site metadata and completion
const chatInfo = await client.getEmbeddedChatInfo("<chat_id>", embedToken.beta);
const embeddedSessionId = await client.ensureEmbeddedChatSession("<chat_id>", embedToken.beta, {
  quote: true,
});
const chatAnswer = await client.embeddedChat("<chat_id>", embedToken.beta, {
  question: "Hello",
  session_id: embeddedSessionId,
  quote: true,
  stream: false,
});

// Agent shared-site inputs and completion
const agentInputs = await client.getEmbeddedAgentInputs("<agent_id>", embedToken.beta);
const agentAnswer = await client.embeddedAgentChat("<agent_id>", embedToken.beta, {
  id: "<agent_id>",
  query: "Hello",
  inputs: {},
  stream: false,
});
```

Embedded calls use RAGFlow's shared-site routes under `/api/v1/chatbots/*` and `/api/v1/agentbots/*`. They authenticate with the token `beta` value, not the normal API token.

For chatbot completions, RAGFlow creates the embedded session on the first no-session request and returns the assistant prologue instead of answering the user's question. Use `ensureEmbeddedChatSession()` first, or include a known `session_id`, before calling `embeddedChat()` with the real question. The CLI `embed-chat` command performs this bootstrap automatically when `--session` is omitted.

## LLM Models

```javascript
// List available models
const models = await client.listModels({ include_details: true });
// Returns: { groups: [...], total: <n> }
```

RAGFlow v0.26.0 exposes model discovery at `/v1/llm/my_llms`. Authentication uses `RAGFLOW_API_KEY`.

Use model names plus provider suffixes when creating resources, for example `qwen-turbo@Tongyi-Qianwen` for `llm_id` and `text-embedding-v4@Tongyi-Qianwen` for `embedding_model`. Some deployments return numeric `id` fields from `/v1/llm/my_llms`; those are server row IDs and should not be sent as `llm_id`.

## Tenant Models (v0.26.0)

These methods use the `/api/v1/models` routes and authenticate with `RAGFLOW_API_KEY`.

```javascript
// List the tenant's added models, optionally filtered by type
const added = await client.listAddedModels({ type: "chat" });
// GET /api/v1/models?type=chat -> { models: [...] }

// List the tenant's default models
const defaults = await client.listDefaultModels();
// GET /api/v1/models/default -> { default_models: [...] }

// Set (or clear) the default model for a type
await client.setDefaultModel({
  model_type: "chat",          // required: chat | embedding | rerank | asr | vision | tts | ocr
  model_provider: "OpenAI",    // omit provider/instance/name to clear the default
  model_instance: "default",
  model_name: "gpt-4o",
});
// PATCH /api/v1/models/default
```

## Model Providers (v0.26.0)

RAGFlow v0.26.0 adds provider/instance/model management under `/api/v1/providers`. All methods authenticate
with `RAGFLOW_API_KEY`. Path segments are URL-encoded, so model identifiers containing `@` or `/` are handled
automatically.

```javascript
// List configured providers, or system-available providers with { available: true }
await client.listProviders({ available: true });        // GET /api/v1/providers?available=true
await client.getProvider("OpenAI");                      // GET /api/v1/providers/OpenAI
await client.addProvider("OpenAI");                      // PUT /api/v1/providers { provider_name }
await client.deleteProvider("OpenAI");                   // DELETE /api/v1/providers/OpenAI

// Discover a provider's models (some providers fetch a live list from the remote API)
await client.listProviderModels("OpenAI", { api_key: "sk-...", base_url: "" });

// Instances hold a set of credentials (multiple API keys per provider are supported)
await client.listProviderInstances("OpenAI");
await client.getProviderInstance("OpenAI", "default");
await client.createProviderInstance("OpenAI", {
  instance_name: "default",    // required
  api_key: "sk-...",           // required
  base_url: "",
  region: "",
  model_info: [],
});                                                       // POST /api/v1/providers/OpenAI/instances
await client.deleteProviderInstances("OpenAI", ["default"]);

// Test a provider connection / API key without persisting an instance
await client.verifyProvider("OpenAI", { api_key: "sk-...", base_url: "", region: "default" });

// Manage the models on an instance
await client.listInstanceModels("OpenAI", "default", { supported: true });
await client.addInstanceModel("OpenAI", "default", {
  model_name: "gpt-4o",        // required
  model_type: "chat",          // required
  max_tokens: 8192,
  extra: {},
});
await client.setInstanceModelStatus("OpenAI", "default", "gpt-4o", "enable"); // PATCH .../models/<name>
```

Treat `api_key` values as sensitive: pass them in, but do not echo them back to the user.

## System

```javascript
// Get the server version
const version = await client.getSystemVersion();

// Inspect and update log levels
const levels = await client.getLogLevels();
await client.setLogLevel("ragflow", "DEBUG");
```

## Utility

```javascript
// Validate connection to RAGFlow server
const ok = await client.validateConnection();
// Returns: true | false
```

## Configuration

Set the following environment variables to configure the API client:
```bash
export RAGFLOW_URL=https://your-ragflow-instance.com
export RAGFLOW_API_KEY=ragflow-xxxxx
```

`RAGFLOW_URL` should be the server root, for example `http://127.0.0.1:9380`. Bare hosts such as `localhost:9380` are normalized to `http://localhost:9380`. The client adds `/api/v1` for REST endpoints and `/v1` for model discovery.

### Security Best Practices

- **Production: Use HTTPS.** Set `RAGFLOW_URL=https://...` for production deployments to protect the API key in transit.
- **Least-privilege keys.** Create dedicated API keys with minimal permissions for specific workflows rather than using admin-level keys.
- **Protect secrets.** Never commit `RAGFLOW_API_KEY` to version control. Use environment variables or a `.env` file that is excluded from git.
