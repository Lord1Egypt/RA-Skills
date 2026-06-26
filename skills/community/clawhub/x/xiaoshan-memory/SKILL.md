---
name: xiaoshan-memory
description: "XiaoShan Memory Engine - Persistent AI memory with semantic search and knowledge graph. Triggers: remember/search memory/recall/forget/knowledge graph/memory stats/记住/搜索记忆/知识图谱/删除记忆"
version: "3.3.0"
trigger_keywords:
  - remember
  - search memory
  - recall memory
  - knowledge graph
  - memory stats
  - forget
  - delete memory
  - memory engine
  - 记住
  - 搜索记忆
  - 知识图谱
  - 删除记忆
exclude_when:
  - User wants to browse web pages
  - User wants to search the internet
  - User wants to send email
  - User wants to manage local files
---

# XiaoShan Memory Engine ⛰️

Persistent memory for your AI — semantic vector search, knowledge graph, and analytics.

## Install

```bash
npx clawhub@latest install xiaoshan-memory --force
```

> **Note:** VirusTotal flags all memory-engine skills as "suspicious" due to keywords like "search" and "forget" in the description. This is a known false positive. The skill is safe — feel free to review the code before installing.

After installation, configure your AI provider:

```bash
# Option A: Set environment variable
export OPENAI_API_KEY=sk-your-key

# Option B: Edit config file
# ~/.xiaoshan/config.yaml
```

## Core API

Server runs at `127.0.0.1:18790` by default.

| Endpoint | Method | Description |
|----------|--------|-------------|
| /save | POST | Save a new memory |
| /search | POST | Search memories semantically |
| /ask | POST | Ask question over memories |
| /stats | GET | Get memory statistics |
| /list | GET | List recent memories |
| /kg/stats | GET | Knowledge graph stats |
| /forget | POST | Delete a memory |

## Provider Support

OpenAI · Zhipu AI · DeepSeek · Ollama (local, no key needed)

## Decision Guide

| User says | Action |
|-----------|--------|
| "Remember this / 记住" | POST /save |
| "What did I say about X" | POST /search |
| "How many memories" | GET /stats |
| "Delete that memory / 删除记忆" | POST /forget |
| "Knowledge graph / 知识图谱" | GET /kg/stats |
