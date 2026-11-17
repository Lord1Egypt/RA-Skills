# gcal over MCP

When `gcal <profile> mcp serve` is connected, it serves three tools instead of a shell: `gcal_tools_search` finds a
command by what it does, `gcal_read` runs a command that only reads, and `gcal_write` runs one that changes Google
Calendar. Each takes `command` (such as `events list`) and `arguments` named as in the command's help, and answers the
same JSON as `--json`.

- `api call`, `calendars.clear`, `session` and `mcp` are not offered; ask the owner to run them. Nor are
  `calendars add` and `calendars remove`, and `mcp.authority` refuses installing or removing a reminder timer.
- A delete that asks at a terminal runs over MCP without a question: make one only when the owner asked for it.
- For ChatGPT or Claude in the browser or on a phone, the owner serves it with `mcp serve --http` behind an HTTPS
  tunnel and a one-time login code; point them to the
  [guide](https://github.com/WireCatLabs/gcal-cli/blob/main/docs/remote.md) rather than setting it up yourself.
