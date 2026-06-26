---
name: dynamic-tool-policy
description: |
  Intent-based tool selection. Activate when you want to know which tools are relevant for the current user message (weather→exec, document→feishu_doc, search→web_search). Reduces context and avoids tool loops.
---

# Dynamic Tool Policy

**When to use:** Before calling many tools, or when the user message is about weather, search, documents, or Feishu — call `get_recommended_tools` with the latest user message to get a short list of recommended tools and a hint.

**Intent mapping:**
- 天气 / weather / wttr → use **exec** (e.g. `curl wttr.in/<city>?format=3`)
- 搜索 / search → use **web_search** once, then reply; do not call web_search again in the same turn
- 文档 / create doc / 飞书文档 → use **feishu_doc** only when the user explicitly asks for a document
- 读文件 / read file → **read**; 写/编辑 → **write**

**Tool:** `get_recommended_tools({ user_message })` → returns `recommended_tools` (array of tool names) and `hint` (short instruction).
