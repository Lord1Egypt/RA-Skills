# supermemory — AI Memory Engine

Semantic memory layer powered by vector search. Store, recall, and connect conversation insights across all customer interactions.

## Architecture
```
Conversation → Extract Insights → Embed → Store (Vector DB)
                                            ↓
Query → Semantic Search → Relevant Memories → Inject into Context
```

## Memory Types
| Type | TTL | Example |
|------|-----|---------|
| Customer Fact | Permanent | "Ahmed from Dubai, buys 50 units/quarter" |
| Conversation Insight | 90 days | "Interested in bulk pricing for Model X" |
| Market Signal | 30 days | "East Africa demand spike for product Y" |
| Effective Script | Permanent | "Opening with local market data → 3x reply rate" |

## Commands
- `memory:add <text>` — Manually add a memory
- `memory:search <query>` — Semantic search across all memories
- `memory:list [type]` — List recent memories by type
- `memory:forget <id>` — Delete a specific memory
- `memory:stats` — Memory usage statistics

## Auto-Capture
When enabled, the engine automatically extracts and stores:
1. Customer preferences and requirements
2. Price sensitivity signals
3. Competitive mentions
4. Purchase timeline indicators
5. Relationship context (referrals, prior interactions)

## Configuration
```json
{
  "provider": "lancedb",
  "embedding_model": "{{embedding_model}}",
  "auto_capture": true,
  "capture_strategy": "last_turn",
  "recall_top_k": 5,
  "ttl_days": {
    "customer_fact": null,
    "conversation_insight": 90,
    "market_signal": 30,
    "effective_script": null
  }
}
```

## Integration
Works with:
- **LanceDB** (local, no external dependency)
- **Supermemory Cloud** (hosted, API key required)
- **Memos** (self-hosted note-taking)
