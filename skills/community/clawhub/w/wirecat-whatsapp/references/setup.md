# Linking, installation, MCP and troubleshooting

## First setup

These instructions are available through `wa skill show` without a linked device. On a new installation, read them
first, then `wa setup --help` for the linking choices and `wa commands --json` for the command tree.
`wa skill install --for all` installs these instructions separately without linking.

When the owner asks to connect WhatsApp, tell them: "Allow about five minutes. Your phone sends your recent chats
once, right after linking; older messages can be asked of it one chat at a time." Ask which profile name they want;
never pick one.

- **The owner has a terminal:** `wa personal setup --agent claude` (or `codex`, `cursor`, `gemini`, `all`, `none`)
  in their own terminal. It checks the computer, links, reads the account and shows five chats.
- **You have no terminal:** run `wa personal session start qr` (or `wa personal setup --agent claude --json`) in
  the background — it waits up to 5 minutes for the scan, and a shell tool shows nothing until it exits. Read its
  output and paste the QR text block into the chat as a code block, exactly as printed, for the owner to scan in
  WhatsApp → Settings → Linked devices → Link a device. WhatsApp renews the code after 60 seconds and then about
  every 20 seconds: paste each new block at once and say the old one expired. With `--json` each code is also a
  stderr line `{"event":"qr","qr":{"text",…}}`. Linking is not on MCP; with only MCP, ask the owner to run it
  or to link from WireCat Desktop (Tools → WhatsApp → Manage).
- **Never ask for the phone number or a pairing code in the chat.** A pairing-code link (`--method phone`, or
  `session start phone`) is for the owner to run in their own terminal.

A profile linked before is checked without linking again, and nothing is asked. Do not link a profile twice: a new
link is a new device on the owner's phone. After linking, the phone sends history in parts for
several minutes, only while WhatsApp is open on it, and only `serve` saves the late parts: suggest
`wa personal server install` and keeping the phone open — install it only when the owner agrees.

## Installation readiness

A global npm install installs this skill and, as a separate small package, the engine that speaks WhatsApp's
protocol. `wa doctor` says whether the engine is found. Read `wa skill show` and verify your skill is loaded before
linking. If your process predates installation, refresh your shell PATH yourself; do not ask the owner to edit PATH.

## Moved folders

**`WA_CONFIG_DIR`, `WA_STATE_DIR` and `WA_CACHE_DIR` move the device keys too.** With them a profile looks for
another device and may answer "not linked" although the owner linked it. `wa config show` says whether they are set.
Do not link again; ask the owner.

## MCP

An agent that cannot run commands (a chat app such as Claude Desktop, a remote agent) uses the MCP server instead:
`wa personal mcp serve`. When you can run commands, use the commands instead of MCP.

- MCP uses `wa_tools_search`, then `wa_read` or `wa_write` with `{command, arguments}`, the CLI path such as
  `messages list`. There are no forms and no confirmation form; the profile's `permissions` decide which commands it
  offers, the same as on the command line, and `ask` permits the requested MCP write.
- **An agent never deletes for everyone**, at any level: `messages delete` through MCP is for the owner only (`wa`
  asks WhatsApp to take the messages from the owner's devices; not yet checked on a phone) and has no
  `--for-everyone`. Deleting for everyone stays the owner's `wa personal messages delete --for-everyone`.
- `wa personal mcp config` prints the entry with full paths.
- `wa personal mcp serve --http --public-url https://laptop.example.ts.net` (the owner's own tunnel address) serves
  behind the owner's tunnel with its own login.
- An open MCP server holds the connection for two minutes after its last call ([connection](connection.md)).
- Never change permissions to get round a refusal. Guide:
  [MCP](https://github.com/WireCatLabs/whatsapp-cli/blob/main/docs/mcp.md).

## Before reporting a bug

Compare `wa -V` with `npm view @wirecat/whatsapp-cli version`. An older install may lack the fix.
`wa personal doctor` shows whether the engine is installed, whether the device keys exist with private file modes,
and who last held the lock.
