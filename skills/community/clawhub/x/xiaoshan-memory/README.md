# XiaoShan Memory Engine

Persistent AI memory — semantic vector search, knowledge graph, and analytics.

## Install

```bash
npx clawhub@latest install xiaoshan-memory
```

## Setup

1. Configure AI provider in `~/.xiaoshan/config.yaml`
2. Start server: `python scripts/start_server.py`
3. Activate: `python scripts/activate.py <LICENSE_KEY>`

## API

Server runs at `127.0.0.1:18790`

| Endpoint | Method | Description |
|----------|--------|-------------|
| /save | POST | Save a memory |
| /search | POST | Semantic search |
| /ask | POST | Q&A over memories |
| /stats | GET | Memory statistics |
| /forget | POST | Delete a memory |

## Providers

OpenAI · Zhipu AI · DeepSeek · Ollama (local)

## License

MIT
