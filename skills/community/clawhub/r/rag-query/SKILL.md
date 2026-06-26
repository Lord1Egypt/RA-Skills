---
name: rag-query
description: Query the RAG knowledge base (Qdrant kb_main) by semantic search. Returns top-k chunks with text, doc_id, source, text_type, topic_tags.
metadata: { "openclaw": { "emoji": "🔎", "requires": { "bins": ["node"], "env": ["QDRANT_URL", "EMBED_API_KEY"] }, "primaryEnv": "QDRANT_URL" } }
---

# rag-query

## Usage

```bash
# 最简单：位置参数作为查询
node skills/rag-query/scripts/query.mjs "渗透测试流程"

# 显式传参 + 控制 top-k 和 topic-tags
node skills/rag-query/scripts/query.mjs \
  --query "TCP/IP 模型" \
  --top-k 5 \
  --topic-tags "net_basic,protocol"
```

## Parameters

| Param           | Required | Example                       | Description                                |
|----------------|----------|-------------------------------|--------------------------------------------|
| `--query`      | yes*     | `"渗透测试流程"`            | 查询字符串；也可以作为第一个位置参数     |
| `--top-k`      | no       | `5`                           | 返回片段数量，默认 5                       |
| `--topic-tags` | no       | `"net_basic,protocol"`      | 逗号分隔标签，用于按 topic_tags 过滤       |
| `--collection` | no       | `"kb_main"`                 | Qdrant collection 名称，默认 `kb_main`     |

输出为 JSON 数组，每个元素包含 `text`、`doc_id`、`source`、`text_type`、`topic_tags` 字段，可直接注入 Agent 上下文使用。

