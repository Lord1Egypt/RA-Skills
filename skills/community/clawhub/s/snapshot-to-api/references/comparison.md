# Snapshot vs API: Detailed Comparison

## Benchmark: Table Schema Query (54 fields)

### Token Consumption

| Method | Response Size | Useful Info | Context Tokens |
|--------|-------------|-------------|----------------|
| Snapshot | ~45 KB | ~15% | **~15,000** |
| API evaluate | ~3.5 KB | ~90% | **~1,000** |
| **Ratio** | **13x** | **6x** | **15x** |

### End-to-End Timing

| Phase | Snapshot | API evaluate |
|-------|----------|-------------|
| Open page | ~4s | ~4s |
| Fetch data | ~4s (render + serialize DOM) | **2s** (fetch) |
| Transfer to LLM | ~4s (45KB) | **0.5s** (3.5KB) |
| LLM parsing | **Extra round needed** | **0** (already JSON) |
| **Total** | **~12s + 1 extra LLM turn** | **~6.5s, done in 1 turn** |

### Data Completeness

| Method | Complete? | Why |
|--------|-----------|-----|
| Snapshot | ❌ May truncate | Virtual scroll renders only visible rows; large DOM gets truncated |
| API evaluate | ✅ 100% | API returns all data, no UI rendering limits |

## Why 15-20x Fewer Tokens

### 1. Information Density

```
Snapshot (human-readable UI):
  cell "user_id" [ref=e55] → cell "string" [ref=e54] → cell "29" [ref=e57] → cell "-" [ref=e58] × 17 columns

API (machine-readable JSON):
  {"name": "user_id", "type": "string", "comment": "User ID"}
```

Same info: **17 cells + 17 refs** vs **1 line of JSON**.

### 2. No "UI Understanding" Cost

Snapshot requires LLM to:
1. Map columnheaders to cells
2. Parse nested DOM tree structure
3. Filter out navigation, buttons, decorative elements

API returns clean data — LLM **uses it, doesn't interpret it**.

### 3. No UI Rendering Limits

- **Virtual scrolling**: Pages render only 20-30 visible rows
- **Lazy loading**: Some data loads on scroll/click
- **DOM truncation**: Snapshots cap at a size limit

APIs have none of these constraints.

## Cost Projection

For a workflow that queries table schemas 10 times per session:

| Method | Tokens per query | 10 queries | Monthly (20 sessions) |
|--------|-----------------|------------|----------------------|
| Snapshot | 15,000 | 150,000 | 3,000,000 |
| API | 1,000 | 10,000 | 200,000 |
| **Savings** | | | **2,800,000 tokens/month** |
