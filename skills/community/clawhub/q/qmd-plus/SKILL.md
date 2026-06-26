---
name: qmd_plus
description: Enhanced QMD search with LLM-powered query expansion. Better recall and precision for multilingual knowledge bases. Use when users ask to search notes, find documents, or look up information with intelligent query expansion.
license: MIT
compatibility: Requires qmd CLI or MCP server. Install via `npm install -g @tobilu/qmd`.
metadata:
  author: 虾爬爬 (based on qmd by tobi)
  version: "1.0.0"
  slug: qmd-plus
allowed-tools: Bash(qmd:*), Bash(node), Bash(jq), Bash(npx), Bash(your-llm-cli), mcp__qmd__*
---

## ⚠️ 安全与隐私说明

**重要：** 本技能需要将查询发送到外部 LLM 进行扩展。这意味着：

1. **你的查询内容会暴露给 LLM 提供商** — 包括搜索关键词、collection 名称等
2. **不要搜索敏感内容** — 避免查询包含密码、API 密钥、私人数据等
3. **LLM 响应需要人工确认** — 在安装前查看元数据/集成不一致

**运行时指令：**
- 本技能本身**不直接调用 LLM**，而是生成提示词供用户选择 LLM
- 用户需要自行配置 LLM 调用方式（如 `npx @anthropic/claude-code`、`kimi` 等）
- 查询扩展过程在本地完成，只有提示词发送到外部 LLM

**数据流：**
```
用户查询 → 本地生成提示词 → 外部 LLM → JSON 响应 → 本地构造 qmd 查询 → 本地搜索
```

**建议：** 在生产环境使用前，审查 `scripts/expand-query.js` 和 `scripts/qmd-query-llm.sh` 了解数据如何发送。

# QMD Plus - QMD with LLM Query Expansion

Enhanced local search engine for markdown content with intelligent LLM-powered query expansion.

## Install

```bash
# Install via ClawHub
clawhub install qmd-plus

# Or clone manually
git clone <repo> ~/workspace/skills/qmd_plus
```

## Status

!`qmd status 2>/dev/null || echo "Not installed: npm install -g @tobilu/qmd"`

## MCP: `query`

```json
{
  "searches": [
    { "type": "lex", "query": "CAP theorem consistency" },
    { "type": "vec", "query": "tradeoff between consistency and availability" }
  ],
  "collections": ["docs"],
  "limit": 10
}
```

### Query Types

| Type | Method | Input |
|------|--------|-------|
| `lex` | BM25 | Keywords — exact terms, names, code |
| `vec` | Vector | Question — natural language |
| `hyde` | Vector | Answer — hypothetical result (50-100 words) |

### Writing Good Queries

**lex (keyword)**
- 2-5 terms, no filler words
- Exact phrase: `"connection pool"` (quoted)
- Exclude terms: `performance -sports` (minus prefix)
- Code identifiers work: `handleError async`

**vec (semantic)**
- Full natural language question
- Be specific: `"how does the rate limiter handle burst traffic"`
- Include context: `"in the payment service, how are refunds processed"`

**hyde (hypothetical document)**
- Write 50-100 words of what the *answer* looks like
- Use the vocabulary you expect in the result

**expand (auto-expand)**
- Use a single-line query (implicit) or `expand: question` on its own line
- Lets the local LLM generate lex/vec/hyde variations
- Do not mix `expand:` with other typed lines — it's either a standalone expand query or a full query document

### Intent (Disambiguation)

When a query term is ambiguous, add `intent` to steer results:

```json
{
  "searches": [
    { "type": "lex", "query": "performance" }
  ],
  "intent": "web page load times and Core Web Vitals"
}
```

Intent affects expansion, reranking, chunk selection, and snippet extraction. It does not search on its own — it's a steering signal that disambiguates queries like "performance" (web-perf vs team health vs fitness).

### Combining Types

| Goal | Approach |
|------|----------|
| Know exact terms | `lex` only |
| Don't know vocabulary | Use a single-line query (implicit `expand:`) or `vec` |
| Best recall | `lex` + `vec` |
| Complex topic | `lex` + `vec` + `hyde` |
| Ambiguous query | Add `intent` to any combination above |

First query gets 2x weight in fusion — put your best guess first.

### Lex Query Syntax

| Syntax | Meaning | Example |
|--------|---------|---------|
| `term` | Prefix match | `perf` matches "performance" |
| `"phrase"` | Exact phrase | `"rate limiter"` |
| `-term` | Exclude | `performance -sports` |

Note: `-term` only works in lex queries, not vec/hyde.

### Collection Filtering

```json
{ "collections": ["docs"] }              // Single
{ "collections": ["docs", "notes"] }     // Multiple (OR)
```

Omit to search all collections.

## Other MCP Tools

| Tool | Use |
|------|-----|
| `get` | Retrieve doc by path or `#docid` |
| `multi_get` | Retrieve multiple by glob/list |
| `status` | Collections and health |

## CLI

```bash
qmd query "question"              # Auto-expand + rerank
qmd query $'lex: X\nvec: Y'       # Structured
qmd query $'expand: question'     # Explicit expand
qmd query --json --explain "q"    # Show score traces (RRF + rerank blend)
qmd search "keywords"             # BM25 only (no LLM)
qmd get "#abc123"                 # By docid
qmd multi-get "journals/2026-*.md" -l 40  # Batch pull snippets by glob
qmd multi-get notes/foo.md,notes/bar.md   # Comma-separated list, preserves order
```

## HTTP API

```bash
curl -X POST http://localhost:8181/query \
  -H "Content-Type: application/json" \
  -d '{"searches": [{"type": "lex", "query": "test"}]}'
```

## Setup

```bash
npm install -g @tobilu/qmd
qmd collection add ~/notes --name notes
qmd embed
```

---

## 🚀 LLM 查询扩展（QMD Plus）

使用外部 LLM 生成更高质量的查询变体，替代内置的 expand 功能。

### 为什么用 LLM 扩展？

| 内置 expand | LLM 扩展 |
|------------|---------|
| lex 扩展质量不稳定 | 术语更准确 |
| hyde 固定英文 | 可指定语言 |
| 无法利用上下文 | 可结合笔记内容 |
| 模板化生成 | 智能语义理解 |

### 快速使用

假设 skill 安装在 `~/workspace/skills/qmd_plus/`：

```bash
# 方式 1：wrapper 脚本生成提示词
~/workspace/skills/qmd_plus/scripts/qmd-query-llm.sh "汽车测试流程" -c memory-root-main -l zh

# 方式 2：wrapper 脚本执行（传入 LLM 响应）
~/workspace/skills/qmd_plus/scripts/qmd-query-llm.sh --response '{"lex":[...],"vec":[...]}' -c memory-root-main

# 方式 3：手动扩展 + 搜索
node ~/workspace/skills/qmd_plus/scripts/expand-query.js "汽车测试流程" zh
# → 复制 LLM 输出的 lex/vec → 构造 qmd query
```

### 添加到 PATH（可选）

```bash
# 在 ~/.zshrc 或 ~/.bashrc 中添加：
export PATH="$HOME/workspace/skills/qmd_plus/scripts:$PATH"

# 然后可以直接使用：
qmd-query-llm "汽车测试流程" -c memory-root-main -l zh
```

### qmd-query-llm 命令

自动完成：LLM 扩展 → 构造查询 → 执行搜索 → 返回结果

```bash
# 生成 LLM 提示词（Mode 1）
qmd-query-llm "汽车测试流程" -c memory-root-main -l zh

# 执行搜索（Mode 2，传入 LLM JSON 响应）
qmd-query-llm --response '{"lex":["汽车测试","整车试验"],"vec":["测试流程是什么"]}' -c memory-root-main

# 显示评分详情
qmd-query-llm --response '<json>' -c memory-root-main --explain
```

### 脚本直接使用

```bash
# 生成 LLM 提示词
node expand-query.js "汽车测试流程" zh

# 输出示例：
# 你是一个专业的知识库搜索查询优化器...
# （将上述提示词发送给 LLM，获取 JSON 响应）
```

### LLM 响应格式

```json
{
  "lex": ["汽车测试", "整车试验", "VTS 验证"],
  "vec": ["汽车测试流程是什么样的", "整车试验包括哪些步骤"]
}
```

### 构造 qmd 查询

```bash
# 将 LLM 响应转换为 qmd query 格式
qmd query $'lex: 汽车测试\nlex: 整车试验\nvec: 汽车测试流程是什么样的' -c memory-root-main
```

### 代码示例

```bash
#!/bin/bash
# qmd-query-llm wrapper

QUERY="$1"
COLLECTION="${2:-.openclaw}"
LANG="${3:-auto}"

# Step 1: Generate LLM prompt
PROMPT=$(node scripts/expand-query.js "$QUERY" "$LANG")

# Step 2: Call LLM (implement according to your LLM provider)
# ⚠️ 注意：查询会发送到外部 LLM，避免敏感内容
RESPONSE=$(your-llm-cli "$PROMPT")

# Step 3: Parse and execute qmd query
LEX=$(echo "$RESPONSE" | jq -r '.lex[]' | sed 's/^/lex: /')
VEC=$(echo "$RESPONSE" | jq -r '.vec[]' | sed 's/^/vec: /')

qmd query "$(echo -e "$LEX\n$VEC")" -c "$COLLECTION"
```

### LLM 集成示例

**使用 Kimi：**
```bash
RESPONSE=$(kimi --prompt "$PROMPT")
```

**使用 Claude Code：**
```bash
RESPONSE=$(npx @anthropic/claude-code --prompt "$PROMPT" --max-tokens 1000)
```

**使用 OpenClaw 内置模型：**
```bash
RESPONSE=$(openclaw run --model modelstudio/qwen3.5-plus --prompt "$PROMPT")
```

### 最佳实践

1. **中文笔记用中文扩展** — 避免跨语言损失
2. **术语用 lex，概念用 vec** — 组合使用效果最好
3. **指定 collection** — 缩小搜索范围提高准确度
4. **--explain 调试** — 查看哪个变体匹配到了结果
