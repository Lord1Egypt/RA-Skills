---
name: semantic-memory-search
slug: semantic-memory-search
version: 2.0.0
description: 为 OpenClaw 记忆文件添加向量驱动的语义搜索。使用 memsearch 库，支持混合搜索（稠密向量 + BM25)，SHA-256 智能去重，本地 embedding 无需 API Key。
本地运行，完全离线。
每天自动索引。
author: sunnyhot
license: MIT
homepage: https://github.com/sunnyhot/semantic-memory-search
keywords:
  - memory
  - search
  - semantic
  - vector
  - memsearch
metadata:
  openclaw:
    requires:
      bins: ["python3"]
    optionalBins: ["memsearch"]
---

# Semantic Memory Search

为 OpenClaw 记忆文件提供本地语义搜索，无需 API Key。

 使用 `memsearch` 命令行工具。

 支持索引 memory/ 目录和根目录下的 MEMORY.md、USER.md 综文件。

 混合搜索（向量 + BM25 + RRF 重排序) SHA-256 智能去重。

 增量更新。

## 命令令```bash
# 篇引记忆文件（默认）
KMP_DUPLICATE_LIB_OK=TRUE ~/Library/Python/3.14/bin/memsearch index \
  ~/.openclaw/workspace/memory/ \
  ~/.openclaw/workspace/MEMORY.md \
  ~/.openclaw/workspace/USER.md \
  ~/.openclaw/workspace/TOOLS.md \
  ~/.openclaw/workspace/AGENTS.md
```

### 语义搜索

```bash
KMP_DUPLICATE_LIB_OK=TRUE ~/Library/Python/3.14/bin/memsearch search "你的搜索词"
```

### Cron 自动索引

每天 2:30 自动索引，结果推送到 Discord。

 手动索引:`KMP_DUPLICATE_LIB_OK=TRUE ~/Library/Python/3.14/bin/memsearch index` 即可。

 如果没有变更，输出 `已索引 N chunks， 无需操作`。Cron ID: `2ad149da-b593-458f-8eee-5976326b0238`
