# Commands: what WhatsApp can do, discovery, JSON and exit codes

## Discovering commands

Read SKILL.md, then discover only the commands relevant to the task. **`wa commands messages send --json`**
describes one command; **`wa commands messages --json`** describes that group. Both include arguments, options,
global options and exit codes. Use `wa <command> --help` for a shorter explanation. Command words form one path, not
a list of groups: inspect different groups in separate calls. **`wa commands --json`** returns the entire tree when
you need an overview; do not read it in full before every task. `effects.remote: "write"` identifies a write to
WhatsApp; `effects.local: "write"` alone, a write to this machine. `commands --json` connects to no account. Its
`contract` field is the shared JSON contract version; it changes only when response fields change incompatibly.
`wa commands info messages list --json` describes one command's schemas and effects.

## What WhatsApp can do

**The tree is shared with tg and max, and WhatsApp does not have all of it yet.** A command the WhatsApp side cannot
do answers exit `2` with "this messenger cannot …" or "WhatsApp cannot …". Everything that reads the local store
works. Today `wa` connects for:

- linking, the account, older history of one chat (`messages sync`);
- sending text (with `--reply-to`), one file per message or a photo and a video as an album, `messages edit`,
  `messages delete` (for the owner only; `--for-everyone` for everyone), `messages download`, `messages forward`,
  `messages transcribe --local`, `messages star|unstar`, `messages pin|unpin`, `reactions add|remove`,
  `polls create|show|vote|voters` ([sending](sending.md));
- `chats mark-read`, `chats mute|unmute`, `chats archive|unarchive|pin|unpin|mark-unread`, `chats delete|clear` (in a
  terminal they ask first);
- `account update`, `metadata sync`, group admin, `contacts show|block|unblock|lookup|sync|add|rename`,
  `account privacy show|set` ([groups](groups.md));
- `doctor --online`, `serve` and `watch` ([connection](connection.md)).

Not built yet: `chats inspect`, more files in one message than a photo and a video, listing a community's groups or
linking one, `account sessions`, `chats create --channel`. What WhatsApp itself lacks is in [groups](groups.md),
[sending](sending.md) and [search](search.md).

## Machine execution

Use `--json --no-input` for headless work. `--json=id,text` keeps those fields of each list item, with the page and
coverage around them. For ids use `--json=id`. `--max-output-bytes` and `--max-input-bytes` set byte budgets; one-shot
actions default to 30 seconds, changed with `--timeout`. Before a sensitive write, global `--dry-run` checks syntax
and permissions; it opens no connection, reserves no write and leaves targets unresolved. See the
[CLI contract](https://github.com/WireCatLabs/whatsapp-cli/blob/main/docs/cli-contract.md).

## Output

- **In a pipe or with `--json`, stdout carries data only**: one JSON value. Everything else, warnings included, goes
  to stderr. An error that ends the command goes to stderr too, and stdout is then empty.
- **Most lists are an object, not an array**: `{ "items": [...], "page": { "limit": 20, "has_more": true },
  "meta": {...} }`. A single thing is `{ "item": {...}, "meta": {...} }`. A chat's messages page with `--cursor`
  from `page.next`.
- **`--jsonl`**: one object per line, for `jq`. Whether there is more is said on stderr only. For `watch --jsonl`, see
  [connection](connection.md).
- **Ids are always strings.** Pass them back unchanged. A person is usually `…@lid` (WhatsApp's hidden id, for example
  `100000000000001@lid`), a group `…@g.us`. Message ids are strings such as `3EB0A1B2C3D4E5F6A7B8`. The owner's own
  chat has the owner's own id.
- `-v` and `-vv` add detail for a person. The version is `wa -V`.

## Exit codes

Branch on the exit code, then on `error.code` and `error.reason` in the stderr object — never on the text.

- `0` success.
- `2` bad input or something WhatsApp cannot do here.
- `4` not linked (or WhatsApp logged the device out).
- `5` the profile may not do this (its `permissions`; the error names the key), or WhatsApp banned or restricted the
  account (do not retry; tell the owner; `account.reachout-restricted` refuses only new contacts, until the date it
  names).
- `6` not found — a chat, or a message the store lacks.
- `7` the chat is not on the list of allowed recipients, or the change asks first and nobody answered (stop and ask
  the owner).
- `8` a limit (`sends_per_hour`, or WhatsApp's own: `account.rate-limited` holds every write, reactions and read
  receipts too, for 15 minutes).
- `12` another command holds the device (`device.in-use`: stop it or use `serve`), took it over (`device.replaced`),
  the engine stopped (`engine.stopped`), or WhatsApp refuses this version (`client.outdated`: tell the owner to
  update). Never stop the owner's `serve` ([connection](connection.md)).
- `14` **unknown whether the message went**, also when the engine stopped during it ([sending](sending.md)).
