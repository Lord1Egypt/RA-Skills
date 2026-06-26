# Supermemory API Reference

Full reference for operations beyond what the scripts cover.

## SDK Init
```js
const Supermemory = require('supermemory').default;
const client = new Supermemory({ apiKey: process.env.SUPERMEMORY_API_KEY });
```

## Add / Ingest

```js
// Single document
await client.add({
  content: "text or markdown",
  containerTag: "my-agent",
  metadata: { source: "file", key: "value" }
});

// Batch add
await client.documents.batchAdd({
  documents: [
    { content: "...", containerTag: "my-agent" },
    { content: "...", containerTag: "my-agent" },
  ]
});

// Ingest a URL
await client.add({ content: "https://example.com", containerTag: "my-agent" });

// Ingest a conversation
await client.conversations.ingestOrUpdate({
  messages: [
    { role: "user", content: "Hello" },
    { role: "assistant", content: "Hi there" }
  ],
  containerTag: "my-agent"
});
```

## Search

```js
// Semantic search
const results = await client.search({
  q: "your query",
  containerTag: "my-agent",
  threshold: 0.5,   // 0–1, lower = more results
  limit: 10
});

// Search memory entries (low latency, conversational)
const memResults = await client.memories.search({
  q: "your query",
  containerTag: "my-agent"
});
```

## Profile (session startup)

```js
const profile = await client.profile({
  containerTag: "my-agent",
  q: "identity and recent context",
  threshold: 0.4
});

profile.profile.static    // stable facts about the agent/user
profile.profile.dynamic   // recent/episodic context
profile.searchResults.results  // relevant memories
```

## Memory Management

```js
// List memories with history
const list = await client.memories.listWithHistory({
  containerTag: "my-agent",
  limit: 50
});

// Forget (soft delete) a memory
await client.memories.forget({ memoryId: "<id>" });

// Create memory directly (bypasses document ingestion)
await client.memories.create({
  content: "Direct memory text",
  containerTag: "my-agent"
});
```

## Document Management

```js
// List documents
const docs = await client.documents.list({ containerTag: "my-agent" });

// Get a document
const doc = await client.documents.get({ id: "<doc-id>" });

// Delete a document
await client.documents.delete({ id: "<doc-id>" });

// Bulk delete by container
await client.documents.bulkDelete({ containerTags: ["old-container"] });
```

## Container Tags

```js
// Get container settings
const settings = await client.containerTags.getSettings({ containerTag: "my-agent" });

// Merge containers
await client.containerTags.merge({
  sourceTags: ["old-agent"],
  targetTag: "new-agent"
});

// Delete a container (and all its data)
await client.containerTags.delete({ containerTag: "old-agent" });
```

## REST API (curl)

Base URL: `https://api.supermemory.ai`

```bash
# Add a memory
curl -X POST https://api.supermemory.ai/v3/memories \
  -L \
  -H "Authorization: Bearer $SUPERMEMORY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"content": "...", "containerTag": "my-agent"}'

# Search
curl "https://api.supermemory.ai/v3/memories/search?q=query&containerTag=my-agent" \
  -L \
  -H "Authorization: Bearer $SUPERMEMORY_API_KEY"
```

Note: API uses 308 redirects — always include `-L` with curl.
