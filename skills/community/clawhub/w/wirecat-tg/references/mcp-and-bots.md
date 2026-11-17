# MCP and bots

Read when serving tg over MCP, when you reach tg only through MCP tools, or for a bot profile (`tg <bot> bot …`).

## MCP

The command line is the default. MCP is the rare case for a client that cannot run commands (a chat app,
a remote agent): `tg <profile> mcp serve` starts the server, `tg <profile> mcp config` prints the client entry.
One server for several profiles: `tg mcp serve --profiles work,personal` or `--profiles all`; with neither it refuses.
Its permissions are the profile's, the same as on the command line. Prefer the command line when you can run it.
MCP uses `tg_tools_search`, then `tg_read` or `tg_write` with `{command, arguments}`.
Use the CLI path such as `stats messages show`.
Bots use `tg_bot_tools_search/read/write` with commands without `bot`; arguments are the command's options in
snake_case. There are no forms;
profile permissions decide access. Over MCP, `ask` does not ask: it permits the write the owner requested, and only
the MCP client can ask first. Tell the owner to turn on approval for `tg_write` in their client, or to set `readonly`
for a profile that should not write. On the command line `ask` still asks.

An agent without a terminal (Claude Desktop, Cursor) uses the MCP server instead: `tg personal mcp serve`. The
profile's `permissions` decide which commands may run, through `tg_tools_search`, `tg_read` and
`tg_write`. Discovery keeps denied commands and their arguments, marking current unavailability
with a reason and permission key. There is no confirmation form: approval for a write is the MCP client's, so ask
the owner to turn it on. `tg personal mcp config` prints the entry with full paths.

`tg personal mcp serve --http --public-url https://<name>.ts.net` serves behind your tunnel with its own owner-code login;
MCP has no server forms. `deny`/`readonly` block writes; `ask`/`allow` permit the requested write without asking,
so the client's approval is the only prompt.
Repeat `--permission key=level` to tighten permissions for the server; it never loosens them. Never change permissions to bypass a refusal.
`tg personal mcp revoke` forgets browser logins for the profile.

## Bots

`tg <bot> bot me` reads the bot identity (id, name and username); it needs a token and refuses `--offline`. MCP offers `tg_bot_read` (`command: "me"`).
Bot commands print data only on stdout with `--json`, in the same message shape as the account. Bot exit codes:
`4` no bot token or Telegram rejected it, `5` the bot profile's permissions, `6` a chat title the bot has not
seen (use the id), `7` the chat is not on the bot's recipient list or an `ask` level got no answer — tell the
owner the `bot recipients add` command, never add it yourself — `8` the bot's `sends_per_hour`, `14` unknown outcome.

`tg <bot> bot messages sync <chat>` imports a channel or supergroup by message number, read-only over
a separate MTProto bot session. Only when the owner asks. `--until-id <message link>` gives the first
number when neither the bot's copy nor the same profile's personal session knows it. Private
chats and basic groups are refused. Sending and updates stay on the Bot API.

Full native Bot API: all 185 Telegram Bot API 10.3 methods are exposed through
`tg <bot> bot api <kebab-method>`, including operations outside the convenient bot commands. It uses the pinned schema and the same
command builder as MAX. Consult method help; native fields are flags or JSON via `--body`,
`--body-file` or stdin. Native `timeout` is `--poll-timeout`, separate from the command deadline.
Only schema-declared file fields interpret `@path`; text remains literal. Secret fields have no
argv flags: use stdin or a JSON file readable only by its owner. Permissions are
`bot.api.<kebab-method>`; destructive methods, including update acknowledgement and financial
operations, ask by default. Never retry an `outcome_unknown` write.
`get-managed-bot-token` and `replace-managed-bot-token` require `--store-token <profile>`;
returned credentials go only to that profile's OS keyring, after identity verification.
Never ask the owner to paste a credential into argv, print one, or fall back to a plaintext file.
