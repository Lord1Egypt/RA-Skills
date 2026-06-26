# Synapse Layer API Reference

## Python SDK Operations

### remember()

Store memory with full security pipeline.

```python
client.remember(
    content: str,
    agent: str = "default",
    memory_type: str = None,
    importance: int = None,
    tags: list = None,
    project: str = None
)
```

**Returns:** Dictionary with `memory_id`, `trust_quotient`, `sanitized`, `privacy_applied`

**Example:**
```python
result = client.remember(
    "User prefers dark mode",
    agent="mel",
    importance=4,
    tags=["preference"]
)
```

### recall()

Retrieve memories ranked by Trust Quotient.

```python
client.recall(
    query: str,
    agent: str = "default",
    limit: int = 10
)
```

**Returns:** Dictionary with `memories` list, `count`, `query`, `recall_mode`

**Example:**
```python
memories = client.recall("user preferences", agent="mel", limit=5)
```

### search()

Cross-agent memory search.

```python
client.search(
    query: str,
    limit: int = 20
)
```

**Returns:** Dictionary with `results` list, `count`, `query`

### process_text()

Extract events from free-form text.

```python
client.process_text(
    text: str,
    agent: str = "default",
    project: str = None,
    source: str = "mcp"
)
```

**Returns:** Dictionary with `status`, `events_detected`, `results`

### health_check()

Verify system availability.

```python
client.health_check()
```

**Returns:** Dictionary with `status`, `version`, `engine`, `database`, `capabilities`

## MCP Tools (External Clients)

When using MCP via HTTP endpoint (for Claude Desktop, Cursor, etc.):

### save_to_synapse

```json
{
  "name": "save_to_synapse",
  "arguments": {
    "content": "Memory content",
    "agent_id": "agent-name",
    "type": "MANUAL",
    "importance": 5,
    "tags": ["tag1", "tag2"]
  }
}
```

### recall

```json
{
  "name": "recall",
  "arguments": {
    "query": "search query",
    "agent_id": "agent-name",
    "limit": 10,
    "mode": "semantic"
  }
}
```

### search

```json
{
  "name": "search",
  "arguments": {
    "query": "search query",
    "limit": 20
  }
}
```

### process_text

```json
{
  "name": "process_text",
  "arguments": {
    "text": "Free-form text to process",
    "agent_id": "agent-name"
  }
}
```

### health_check

```json
{
  "name": "health_check",
  "arguments": {}
}
```

## Error Handling

All operations may raise exceptions on failure:

```python
try:
    result = client.remember("test", agent="mel")
except httpx.HTTPStatusError as e:
    print(f"HTTP error: {e}")
except Exception as e:
    print(f"Error: {e}")
```

## Common Error Codes

| Error | Description | Action |
|-------|-------------|--------|
| 401 | Authentication failed | Check API key |
| 400 | Invalid request | Verify parameters |
| 429 | Rate limited | Wait and retry |
| 500 | Server error | Check service status |
