# Notify Pattern

Use this pattern every time a `📣 Notify:` callout appears **anywhere in the BAD skill** — including inside the Timer Pattern and Monitor Pattern.

**Always print the message in the conversation** — this keeps the in-session transcript readable regardless of channel configuration.

**If `NOTIFY_SOURCE="telegram"`:** also call `mcp__plugin_telegram_telegram__reply` with:
- `chat_id`: `NOTIFY_CHAT_ID`
- `text`: the message

If the Telegram tool call fails (tool unavailable or error returned):
1. Run `/reload-plugins` to reconnect the MCP server. This is a **built-in Claude Code CLI command** — execute it directly, do NOT invoke it via the Skill tool.
2. Retry the tool call once.
3. If it still fails, set `NOTIFY_SOURCE="terminal"` for the remainder of the session.
