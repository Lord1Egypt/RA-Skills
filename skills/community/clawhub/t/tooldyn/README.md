# Dynamic Tool Policy (Intent-Based Tool Selection)

Recommend which OpenClaw tools to use based on the **last user message**. Reduces context size and prevents tool loops when using **Feishu + Ollama** (or similar) with small models.

## Why use this?

- Sending **all** tools every time can overload small/local models (empty reply, no tool call).
- Sending **only relevant tools** per request keeps the prompt small and the model reliable.
- This skill provides a **hint tool** and documents the **full pattern** (config + optional gateway behavior).

## What this skill provides

- **Tool: `get_recommended_tools`**  
  Call with `user_message` (the latest user text). Returns `recommended_tools` (e.g. `["exec","web_search"]`) and a short `hint` so the agent can prefer those tools for the current turn.

- **Intent mapping (keyword-based):**

  | User intent (keywords)        | Recommended tools   |
  |------------------------------|---------------------|
  | 天气, 温度, weather, wttr    | `exec`              |
  | 文档, 飞书文档, create doc   | `feishu_doc`        |
  | 搜索, 查找, search           | `web_search`        |
  | 读取, 读文件, read file      | `read`              |
  | 写入, 编辑文件               | `write`             |
  | 云盘, drive, 文件夹          | `feishu_drive`      |
  | 群聊, chat                   | `feishu_chat`       |
  | wiki, 知识                   | `feishu_wiki`       |
  | 多维表格, bitable            | `feishu_bitable_*`   |

  `exec` is always included. Max 8 tools per recommendation.

## Config and system prompt (recommended)

For **Feishu + Ollama** setups, use these together with this skill:

1. **Limit DM history** so the model doesn’t see 200+ messages:
   - In `openclaw.json`: `channels.feishu.dmHistoryLimit: 20`

2. **System prompt** (in `channels.feishu.dms.default.systemPrompt` and any per-user overrides) — add:
   - *"For web search: call web_search once for the user's query, then reply with a concise answer. Do not call web_search again in the same turn."*
   - Weather: use `exec` with `curl -s "wttr.in/<city>?format=3"`. Do not use web_search for weather.
   - Feishu doc: only create when the user explicitly asks for a document.

3. **Optional: gateway-level filtering**  
  Full “dynamic tool” behavior (only sending 3–8 tools per request) is currently implemented by **patching** the OpenClaw dist bundle (e.g. `auth-profiles-*.js`): add `getLastUserMessageText`, `selectToolNamesDynamically`, and filter the tool list before building the Ollama request. See the [OpenClaw Feishu Ollama Summary](https://github.com/your-repo/CLawFeishu/blob/main/OPENCLAW-FEISHU-OLLAMA-SUMMARY.md) (or your project’s summary doc) for the exact logic. We hope OpenClaw will support a configurable “dynamic tool selection” or “tool policy” in the future so this can be done without patching.

## Installation (ClawHub)

```bash
/skills install @peter7397/dynamic-tool-policy
```

Or copy this folder into your workspace `skills/` and register in `openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "dynamic-tool-policy": {
        "enabled": true
      }
    }
  }
}
```

## Usage

- The agent can call **`get_recommended_tools`** with the current user message to get `recommended_tools` and `hint`, then prefer those tools for that turn.
- For **full** filtering (model only receives the subset of tools), the gateway must apply the same logic (see “Optional: gateway-level filtering” above).

## License

MIT. Share and adapt for OpenClaw community.
