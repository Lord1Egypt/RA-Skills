---
name: rag-ingest
description: 将 Agent 已解读好的正文写入 Qdrant（kb_main）。仅做 chunk、embedding 和向量写入，不负责抓取与精炼。
metadata: { "openclaw": { "emoji": "🧠", "requires": { "bins": ["node"], "env": ["QDRANT_URL", "EMBED_API_KEY"] }, "primaryEnv": "QDRANT_URL" } }
---

# rag-ingest

## Usage

```bash
# 直接通过 --content 传入正文
node skills/rag-ingest/scripts/ingest.mjs \
  --doc-id "doc-001" \
  --topic-tags "net,security" \
  --content "已解读好的长文本..."

# 从 stdin 读取正文（推荐与 deep-research/summarize 配合）
echo "已解读好的长文本..." | node skills/rag-ingest/scripts/ingest.mjs \
  --doc-id "doc-002" \
  --topic-tags "web,http" \
  --source "https://example.com/article"
```

## Parameters

| Param         | Required | Example                        | Description                          |
|--------------|----------|--------------------------------|--------------------------------------|
| `--doc-id`   | yes      | `doc-001`                      | 文档 ID，用于标识/覆盖同一文档       |
| `--topic-tags` | yes    | `net,security`                 | 逗号分隔标签，用于检索过滤          |
| `--content`  | no       | `"..."`                       | 正文；不传时从 stdin 读取           |
| `--source`   | no       | `"https://example.com"`       | 来源标识，写入 payload.source       |
| `--collection` | no     | `kb_main`                      | Qdrant collection 名称              |

