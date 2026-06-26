# Knowledge Base Search Strategy

## When to Use Each Search Method

| Method | When | Speed | Accuracy |
|--------|------|-------|---------|
| Exact keyword match | User mentions specific product name/SKU | Fastest | Highest for exact names |
| Fuzzy / partial match | User uses informal names, typos | Fast | Good |
| Category filter | User asks by type ("有没有连衣裙") | Fast | Good |
| Semantic (LLM synthesis) | User asks conceptual questions ("适合送长辈的") | Slower | Best for intent |
| Full-text policy scan | User asks about policy edge cases | Medium | Depends on KB quality |

---

## Search Priority Order

For each incoming query:

1. **Check for explicit product name/SKU** — if found, fetch directly
2. **Check FAQ index** — if question closely matches a FAQ, return that answer
3. **Check policy_entries by type** — for return/warranty/promotion queries
4. **Filter products by category + tags** — for browsing/recommendation queries
5. **LLM synthesis** — when none of the above returns a confident match

---

## Using kb_search.py

```bash
python3 scripts/kb_search.py \
  --kb knowledge_base.json \
  --query "白色M码连衣裙还有货吗" \
  --domain products \
  --top 3
```

Returns top-N matching entries with relevance scores.
Use results as context for constructing the final answer.

### Domain values:
- `products` — search product catalog
- `policies` — search policy entries
- `promotions` — search active promotions
- `faqs` — search FAQ pairs
- `all` — search all domains, ranked by relevance

---

## Relevance Scoring (in kb_search.py)

Score = keyword overlap + field weight

| Field | Weight | Rationale |
|-------|--------|-----------|
| `name` | 3× | Most discriminative |
| `tags` | 2× | Intentional lookup terms |
| `description` | 1× | Broad but noisy |
| `category` | 1× | Coarse filter |
| `keywords` | 2× | Policy/FAQ specific |

Threshold: return entries with score ≥ 1. If no entries pass, return empty (trigger unknown response).

---

## Handling Stale Data

Check `meta.last_updated` before answering time-sensitive queries:

| Query Type | Staleness Threshold | Behavior if Stale |
|------------|--------------------|--------------------|
| Inventory | > 2 hours | Add caveat: "截至[time]的数据，建议现场确认" |
| Promotions | > 24 hours | Add caveat: "活动信息以最新公告为准" |
| Product info | > 7 days | No caveat needed (specs rarely change) |
| Policies | > 30 days | No caveat needed |
| Prices | > 24 hours | Add caveat if `sale_price` is set |
