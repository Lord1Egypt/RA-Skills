# Setup, installation and machine use

Read when tg is not installed or logged in, a login or keyring error appears, before headless or scripted use, or before reporting a bug.

## Discovering commands

Read this skill, then discover only the commands relevant to the task. **`tg commands search
messages --json`** describes one command; **`tg commands messages --json`** describes that group.
Both include arguments, options, global options and exit codes. Use `tg <command> --help` for a
shorter explanation. Command words form one path, not a list of groups: inspect different groups
in separate calls. **`tg commands --json`** returns the entire tree when you need an overview;
do not read it in full before every task. `effects.remote: "write"` identifies a write to Telegram;
`effects.local: "write"` alone, a write to this machine. `commands --json` connects to no account. Its `contract` field is the shared JSON contract
version; it changes only when response fields change incompatibly, not with a package upgrade, so
check that field rather than comparing whole outputs. The core SKILL.md holds the traps and boundaries.
For a common task, **`tg guide`** lists scenarios — the commands in order and why each — and
`tg guide <name> --json` gives one as data; `tg commands` without `--json` is the list by section.

## Machine execution

`tg commands info messages list --json` describes one command's schemas and effects.
Use `--json --no-input` for headless work; supply credentials explicitly through a pipe.
`--json=id,text` keeps those fields of each list item, with the page and coverage around them. For ids use
`--json=id`.
`--max-output-bytes` and `--max-input-bytes` set byte budgets; one-shot actions default to 30 seconds,
changed with `--timeout`; background history fetch jobs have no default deadline. Before a sensitive write, global `--dry-run` checks syntax and permissions
before action; it opens no messenger connection, reserves no write and leaves targets unresolved.
See the [CLI contract](https://github.com/WireCatLabs/tg-cli/blob/main/docs/cli-contract.md).

## Output in full

Partial reads and downloads may exit `0`: inspect `complete`, `batch.failed` and `issue`; partial download JSONL adds `batch_summary`. Completed work stays saved; resume unfinished items after the suggested wait.

- **In a pipe or with `--json`, stdout carries data only**: one JSON value. Everything else,
  warnings included, goes to stderr. An error that ends the command goes to stderr too, and stdout is then empty.
- **Most lists are an object, not an array**: `{ "items": [...], "page": { "limit": 20, "has_more": true }, "meta": {...} }`.
  A single thing is `{ "item": {...}, "meta": {...} }`. A chat's messages page with `--cursor` from `page.next`.
- **`--jsonl`**: one object per line, for `jq`. Whether there is more is said on stderr only.
- **Branch on the exit code, not on the text**: `0` success, `2` bad input, `4` not logged in, `5`
  the profile may not do this (its `permissions`; the error names the key — do not work around it),
  or Telegram froze the account or limited its messages as spam (do not retry; tell the owner), `6` not found, `7` the chat is not on the list of allowed recipients, or the change asks first and
  nobody answered (stop and ask the owner), `8` a limit (sends per hour, or Telegram's FLOOD_WAIT —
  the error says how long), `14` **unknown whether the message went** (see [messages](messages.md), Sending).
- `-v` and `-vv` add detail for a person. The version is `tg -V`.

## Installation readiness

Global npm installation installs this skill only with `TG_INSTALL_AGENT` set; `tg skill install --for all` does it later. On Windows,
use the one-call installer from the installation guide: it repairs user and current-shell PATH,
installs the skill even with disabled lifecycle scripts and verifies bare `tg`. Read `tg skill show`
and verify your skill is loaded before login. If your process predates installation, refresh your
shell PATH from the user/machine environment yourself; do not ask the user to edit PATH.

## First setup

These instructions are available through `tg skill show` without a Telegram session. On a new
installation, read them first, then `tg setup --help` for login choices and `tg commands --json`
for the command tree. The CLI's root help and first-run authentication errors point to setup.
`tg skill install --for all` installs these instructions separately without logging in.

When the owner asks to install or connect Telegram, tell them: "Allow about five minutes for
setup. Downloading chat history is a separate step and can take longer." Use `tg personal setup --agent
codex` (any profile name the owner picks in place of `personal`; or `cursor`, `claude`, `gemini`, `all`, `none`) in their local terminal. It checks the
computer, obtains app keys, logs in and verifies five chats. Do not ask the owner to paste login
codes, app hashes or 2FA passwords into the conversation; the terminal prompts for them.
If automatic app registration fails, use `tg personal session start --app browser`, then rerun setup.

An agent without a terminal can log in by QR only with stored app keys and no required 2FA input:
run `tg personal session start qr` (or `tg personal setup --agent codex --json`) in the background,
because it waits for the scan and the shell tool shows nothing until it exits. Read its output and
paste the QR text block into the chat as a code block, exactly as printed. When a new block is
printed, paste it and say the old one expired. With `--json` each code is also a stderr line
`{"event":"qr","qr":{"text","expires_at","scan"}}`. Login is not an MCP tool: with only MCP, ask
the owner to run the command in a terminal or to sign in from WireCat Desktop (Tools → Telegram → Manage).
Existing sessions are checked without a new login. Missing keyring access
requires fixing the environment, not another login. Pick a chat and an amount of history with
the owner before `tg personal messages sync <chat> --last 100`; setup starts no background service.

## Environment traps

- **`TG_CONFIG_DIR`, `TG_STATE_DIR` and `TG_CACHE_DIR` also change the keyring entry.** With them
  the profile looks for another login and may answer "no session" although the owner is logged
  in. `tg config show` says whether they are set.
- **"No app credentials … although it has logged in on this machine"** means the keyring is out
  of reach (cron, ssh, a trimmed environment). Do not log in again — that adds another device;
  set `XDG_RUNTIME_DIR`. `tg personal doctor` shows it.

- **Before reporting a bug, compare `tg -V` with `npm view @wirecat/tg-cli version`** (memo:
  `memo --version`, `@wirecat/cli-memo`). An older install may lack the fix. In a zsh loop over command
  paths, `$c` is not split into words: `tg $c --help` passes `search messages` as one argument; write
  `${=c}`.
