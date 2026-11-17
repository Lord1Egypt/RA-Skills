# Programmatic API (RAGFlow v0.27.3)

## Setup

```javascript
const { createClient } = require("{baseDir}/lib/api.js");
const client = createClient();
```

`createClient()` reads `RAGFLOW_URL` and `RAGFLOW_API_KEY` from the process environment only. It never loads local credential/configuration files. See [configuration](API-MODELS-SYSTEM.md#configuration).

Destructive requests fail with `CONFIRMATION_REQUIRED` before network access by default. After verifying authorization and target scope, create a dedicated client with `const destructiveClient = createClient({ allowDestructive: true });` for starting/stopping parsing, deletion, metadata removal or unscoped metadata updates, and ingestion with `delete: true`. Use that client for the deletion examples below; ordinary clients remain suitable for reads and scoped updates.

## Workflow references

These references contain the full supported method examples and request/response details. All clients use the configured RAGFlow server; token and provider administration are explicit capabilities of this skill.

- [Datasets, documents, parsing and chunks](API-DATASETS.md): `listDatasets()`, `getDataset()`, `createDataset()`, `updateDataset()`, `deleteDatasets()`, `uploadDocuments()`, `listDocuments()`, `getDocument()`, `updateDocument()`, `deleteDocuments()`, `metadataSummary()`, `downloadDocument()`, `downloadDocumentById()`, `previewDocument()`, `startParsing()`, `stopParsing()`, `ingestDocuments()`, `waitForParsing()`, `listChunks()`, `getChunk()`, `addChunk()`, `updateChunk()`, `deleteChunks()`, `getDocumentStructureGraph()`, `deleteDocumentStructureGraph()`.

- [Retrieval, metadata, connectors and indexing](API-RETRIEVAL.md): `retrieve()`, `updateMetadata()`, `listConnectors()`, `createConnector()`, `getConnector()`, `updateConnector()`, `deleteConnector()`, `runRaptor()`, `traceRaptor()`, `getKnowledgeGraph()`, `runGraphRag()`, `traceGraphRag()`, `deleteKnowledgeGraph()`.

- [Chat, agents, sessions and embedded access](API-CHAT-AGENTS.md): `listChatAssistants()`, `getChatAssistant()`, `createChatAssistant()`, `updateChatAssistant()`, `patchChatAssistant()`, `deleteChatAssistants()`, `listSessions()`, `createSession()`, `getSession()`, `updateSession()`, `deleteSessions()`, `chat()`, `chatSession()`, `listAgents()`, `getAgent()`, `createAgent()`, `updateAgent()`, `deleteAgents()`, `listAgentTags()`, `updateAgentTags()`, `listAgentSessions()`, `createAgentSession()`, `deleteAgentSessions()`, `agentChat()`, `ensureEmbedToken()`, `listSystemTokens()`, `createSystemToken()`, `deleteSystemToken()`, `getEmbeddedChatInfo()`, `ensureEmbeddedChatSession()`, `embeddedChat()`, `getEmbeddedAgentInputs()`, `embeddedAgentChat()`.

- [Model providers and server configuration](API-MODELS-SYSTEM.md): `listModels()`, `listAddedModels()`, `listDefaultModels()`, `setDefaultModel()`, `listProviders()`, `getProvider()`, `addProvider()`, `deleteProvider()`, `listProviderModels()`, `listProviderInstances()`, `getProviderInstance()`, `createProviderInstance()`, `deleteProviderInstances()`, `verifyProvider()`, `listInstanceModels()`, `addInstanceModel()`, `setInstanceModelStatus()`, `getSystemVersion()`, `getSystemHealth()`, `getLogLevels()`, `setLogLevel()`, `validateConnection()`.

For CLI syntax use [COMMANDS.md](COMMANDS.md). `agentChat()` normalizes `workflow_finished` results with `stream: false`; `chatSession()` preserves submitted history only when `pass_all_history_messages` is enabled. Downloads return base64 bytes, not URLs. Destructive clients are never a substitute for verifying user authorization.
