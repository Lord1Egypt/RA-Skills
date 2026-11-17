---
name: speculative-exec
description: Speculative execution engine — predict and pre-load context the agent is likely to need next. Distilled from Claude Code speculation module.
metadata:
  openclaw:
    requires:
      bins: [python3]
---

# Speculative Exec

Distilled from Claude Code speculation module. Predicts the next likely action
and pre-loads the needed context in parallel with LLM response generation.
Reduces perceived latency by 30-60% for common workflows.

## When to use

- User asks to "analyze" something → pre-load data sources
- User asks to "read" a file → pre-load the file content
- User asks to "search" → pre-load search index
- User asks to "compare" → pre-load both items
- User asks to "write" a report → pre-load template
- Any repetitive workflow where the next step is predictable

## How it works

1. **Pattern Recognition** — Match user intent against known workflow patterns
2. **Context Prediction** — Predict what files/data/tools will be needed
3. **Pre-load Queue** — Start loading predicted resources in background
4. **Cache Delivery** — When the agent actually needs the resource, serve from cache

## Usage

```bash
# Start speculative pre-load based on user message
python3 {baseDir}/speculator.py --message "帮我分析这个股票"

# Predict next actions from conversation history
python3 {baseDir}/speculator.py --history conversation.json

# Train on custom workflow patterns
python3 {baseDir}/speculator.py --train workflows.json

# Check cache status
python3 {baseDir}/speculator.py --status
```

## Output

```json
{
  "prediction": "read_stock_data",
  "confidence": 0.92,
  "preloaded": ["stock_price", "financial_report", "news"],
  "estimated_save_ms": 1200
}
```

## Built-in workflow patterns

| Intent Pattern | Predicted Next Action | Pre-loads |
|---------------|----------------------|-----------|
| 分析/analyze | Read data source | Data files, reports |
| 对比/compare | Read both items | Item A, Item B |
| 搜索/search | Search index | Index files |
| 写/write | Template + context | Templates, examples |
| 修改/edit | Read target file | Target file |
| 安装/install | Read docs | Documentation |
| 测试/test | Read test files | Test files, fixtures |
| 部署/deploy | Read config | Config files |

## Algorithm reference

Based on Claude Code speculation module:
- Intent classification via keyword + regex patterns
- Weighted prediction scoring
- Parallel pre-load with timeout
- Cache invalidation on context change
- Confidence threshold gating (default: 0.7)
