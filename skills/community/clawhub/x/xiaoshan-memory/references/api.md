# XiaoShan Memory Engine - HTTP API Reference

Server: `127.0.0.1:18790`

All endpoints require authentication header.

## Endpoints

### POST /save
Save a new memory.
Request: `{"content": "...", "memory_type": "semantic", "importance": 0.8}`

### POST /search
Search memories semantically.
Request: `{"query": "...", "limit": 5}`

### POST /ask
Ask a question over your memories.
Request: `{"question": "...", "limit": 5}`

### GET /stats
Get memory statistics.

### GET /list
List recent memories. Query params: `limit`, `offset`

### POST /kg/query
Query knowledge graph.
Request: `{"entity": "...", "depth": 1}`

### POST /forget
Delete a memory.
Request: `{"memory_id": 42}`

### GET /export
Export memories as report.

## Trigger Patterns

| User Says | Endpoint |
|-----------|----------|
| "记住 X" | POST /save |
| "搜索记忆" | POST /search |
| "知识图谱" | POST /kg/query |
