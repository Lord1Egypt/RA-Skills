# memo — MCP server and permissions

Local clients use stdio; remote clients can use `memo mcp serve --http --public-url <https-origin>` behind the owner’s
HTTPS tunnel and cli-core’s access-code OAuth login. Both expose the same commands and permission checks.
`memo mcp revoke` logs every remote app out; use the same Memo state environment as the server.

MCP offers `memo_tools_search`, `memo_read` and `memo_write`, using CLI paths and advertised snake_case arguments.
Saved dotted `permissions` keys apply to commands. `deny` keeps a command visible but unavailable,
`readonly` allows reads, and `ask` or `allow` permits a write. `ask` runs without a terminal question over MCP:
respect the owner's existing authorization before acting. `mcp.authority` defaults to `deny` for source-folder and mail-rule
changes. `MEMO_READ_ONLY=1` marks writing commands unavailable and refuses calls. `--permission key=level` can only tighten saved levels.
Find command arguments before calling them. Through `memo_read`, open a cited note with `notes show`
(`note: ref`) or a message/email with `messages show` (`message: ref`, `full: true` for whole attachment text).

`MEMO_GROUP_LOCK=<group>` pins the server to one account group, and it fails closed. Only these run: `context`, `show`,
`messages show`, `search all|messages|mail|notes|people`, `groups list`, `tags add|remove`, the `deals`, `leads`,
`organizations`, `pipelines list|show`, `memories`, `facts`, `actions`, `review` and `tasks` commands,
`projects list|add|context|status|key-documents`, `people list|add`, `notes list|show`,
`relationships list|add|roles list`. Everything else is
`permission_error`. Your memories, facts and the owner's notes and tasks show in every group; a reference, a bare id of
one, another group, `--source all` or an account outside the group is `permission_error`. Do not read around it; say
which group you were given when a question needs more.
