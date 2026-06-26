---
name: context-mode
description: context-mode is an MCP server that saves 98% of your context window by sandboxing tool outputs. It routes large file reads, shell outputs, and web fetches through SQLite + FTS5 instead of flooding the context. Also provides session continuity across context compactions via BM25 retrieval.
triggers:
  - 分析项目
  - 有多少文件
  - 帮我研究
  - 检查更新
  - token 节省
  - 上下文压缩
  - context overflow
  - 帮我搜索
tags:
  - token-optimization
  - context-management
  - mcp
  - productivity
compatibility: openclaw | claude-code | vscode-copilot | cursor | gemini-cli
license: ELv2
source: https://github.com/mksglu/context-mode
---

# Context Mode

An MCP server that solves the context window problem in AI coding agents. It provides:
1. **Context Saving** — sandbox tools keep raw data out of context window
2. **Session Continuity** — SQLite + FTS5 for event tracking
3. **Think in Code** — program analysis instead of reading files
4. **Output Compression** — terse output format reducing tokens 65-75%

## Available Tools

| Tool | When to Use | Token Savings |
|------|-------------|---------------|
| `ctx_batch_execute` | Run multiple commands + auto-search results | 90%+ vs raw exec |
| `ctx_execute` | Single script execution (JS/Python/Shell) | 90%+ vs raw exec |
| `ctx_execute_file` | Run code from a file, return only result | high |
| `ctx_index` | Index docs/knowledge into searchable FTS5 | — |
| `ctx_search` | Search indexed content with BM25 | fast recall |
| `ctx_fetch_and_index` | Fetch URL + index into knowledge base | 90%+ vs raw web fetch |

## Decision Rules

### Use ctx_batch_execute instead of multiple exec/read calls when:
- Analyzing multiple files at once
- Counting/grepping across many files
- Need command output + search results together

### Use ctx_execute instead of reading files when:
- User asks "how many lines/funcs/classes in X"
- Need to compute something, not just read it

### Use ctx_fetch_and_index instead of web_fetch when:
- Researching a topic across multiple pages
- Full raw content won't fit in context

## Output Format

Terse. Drop filler, pleasantries, hedging.
```
❌ "So I ran a command to check the files and found that there are..."
✅ "Checked. 3 TypeScript files: src/index.ts (142 lines), src/cli.ts (89 lines)."
```

## OpenClaw Integration

Install via MCP:
```bash
openclaw mcp set context-mode '{"command":"npx","args":["-y","context-mode"]}'
openclaw gateway restart
```
