# Chat, agents, sessions and embedded access (v0.27.3)

[API overview](API.md)

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
await destructiveClient.deleteChatAssistants(["<chat_id1>", "<chat_id2>"]);
```

## Session

```javascript
// List sessions for a chat assistant
const sessions = await client.listSessions("<chat_id>", { page: 1 });

// Create a session
const session = await client.createSession("<chat_id>", { name: "Q&A Session" });

// Inspect or rename a session
const current = await client.getSession("<chat_id>", "<session_id>");
await client.updateSession("<chat_id>", "<session_id>", { name: "Reviewed Q&A" });

// Delete sessions by IDs
await destructiveClient.deleteSessions("<chat_id>", ["<session_id1>"]);
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

`chatSession()` uses `POST /api/v1/chat/completions` with `chat_id` and `session_id` in the JSON body. Use `session_id` for session identity. By default, only the latest user message is appended to the stored history. Set `pass_all_history_messages: true` to replace the entire history with the submitted messages array. The client only supports the current streaming format.

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
await destructiveClient.deleteAgents(["<agent_id1>"]);
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
await destructiveClient.deleteAgentSessions("<agent_id>", ["<session_id1>"]);
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
await destructiveClient.deleteSystemToken(newToken.token);

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

