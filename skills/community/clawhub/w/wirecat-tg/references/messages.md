# Reading and sending messages

Read before a send, edit, forward, reply, draft, scheduled message, attachment, forum topic or a change to the chat list.

## Reading

The ids below are made up — use the real ones from the previous answer.

```sh
tg personal chats list --json                      # find a chat, take its id
tg personal chats list 'title:*vale* kind:group unread_count>0' --offline --json  # filtered, from the local store
tg personal chats events -1001234567890 'time>=7d' --json  # who joined, left, was added or removed
tg personal chats members list -1001234567890 --json  # a group's members, paged
tg personal reactions list -1001234567890 4242 reaction:🔥 --json  # who reacted; refused (reason reactions.*) where the chat hides it
tg personal chats inspect https://t.me/+AbCd --json  # where an invite leads, without joining
tg personal topics list -1001234567890 --json        # a forum's topics; a message's threadId is one of them
tg personal topics show -1001234567890 12 --json     # one topic: title, closed, pinned, last activity
tg personal chats show -1001234567890 --json       # one chat and who is in it
tg personal contacts show @ivan --json             # one person and the chats shared with them
tg personal messages list -1001234567890 --limit 20 --json  # the latest messages, oldest first
tg personal messages list -1001234567890 'id<4242' --json  # older ones
tg personal messages list -1001234567890 'id>4242' --json  # newer ones, oldest first; 'date>2h' reads from a time
tg personal messages context -1001234567890 4242 --before-n 3 --after-n 3 --json
```

- **A page number over a live list can repeat or skip a row.** The newest is on top, so a message
  arriving between page one and page two moves someone across the boundary. A chat's messages do
  not have this: `--cursor` from `page.next` is exact.

## Sending

Before a sensitive write, global `--dry-run` checks syntax and permissions before action; it opens no
messenger connection, reserves no write and leaves targets unresolved.

- **Exit `14` means an unknown write outcome, not permission to replay it.** Inspect
  `tg personal sends list --json` by `operation_id` and the target chat's history. `operation_id` correlates
  the journal; it is not an idempotency key. Retry a message only when the provider's confirmed
  deduplication contract applies to the same chat, topic, content and `--operation-id`.
  Never automatically repeat an unknown write based only on its error code.

- **Multi-line text goes through stdin only.** Leave out the last argument and the text is read
  from input: `printf 'first\n\nthird' | tg personal messages send me`.
- **`--md` uses Telegram syntax:** `**bold**`/`*bold*`, `_italic_`, `__underline__`,
  `~~strike~~`/`~strike~`, `||spoiler||`, code/fences, links and `> ` quotes.
  Styles nest; code/pre cannot overlap other formatting, and quotes cannot nest. MAX has different rules.
  Without the flag text is literal. Use http/https/mailto links; no unsafe URL schemes.
- **`--at-time 2h` or `--at-time 2026-10-01T09:00` (local time) hands the message to Telegram to send later.**
  It is never repeated: `--operation-id` is refused with it, and after exit `14` look in
  `tg personal messages scheduled <chat>` — a second send would be a second message.
- **A scheduled message has its own id, from `tg personal messages scheduled <chat>`.** The same number in the
  chat's history is another, sent message, so `messages edit` and `messages delete` never take it. Use
  `messages scheduled cancel <chat> <id>`, `messages scheduled edit <chat> <id> [text] [--at-time 2h]` (only the
  time, only the text, or both) and `messages scheduled send <chat> <id>` (sends it now, under a new id).
- **`--photo <path>` or `--file <path>` attaches a file, the text as its caption.**
  Repeat for an album of up to ten items: photos/videos together, or documents only. The caption goes
  on the first item; every item counts toward the hourly limit. JSON returns all `messages`. A photo is
  recompressed by Telegram; a file goes byte for byte. Hidden files and folders, SSH keys, tg's own
  folders and the message store are refused — only the owner adds `--allow-any-file`. A retry with
  the same `--operation-id` is safe here too (measured 2026-09-29).
- **Forum sends:** `messages send --topic`, `messages forward --topic` and `polls create --topic` use a topic id
  from `topics list` (for a forward, a topic of the `--to` chat); `topics show <chat> <id>` reads one topic.
  Reply targets must belong to that topic. Keep the same chat, topic and `--operation-id` on a retry;
  never retry a scheduled send. Missing or closed topics are refused; nothing marks them read.
- **Posting as a channel:** `messages send --send-as <id>` only with an id from `chats send-as <chat>`,
  and only when the owner named that identity; `messages forward` and `polls create` take it too. A retry
  keeps the same `--send-as`.

## Telegram drafts

`tg personal messages send CHAT "text" --draft` saves a draft for the owner to review and send in Telegram.
It replaces any existing draft in that chat/topic, so confirm the intended replacement when needed.
It sends no message and uses the separate `drafts` permission. Formatting, `--reply-to`, `--topic` and
`--no-preview` work; empty text, attachments, scheduling and other send-only flags are refused.
The receipt has `saved: true`; never describe it as a sent message. Clearing drafts is not exposed.

## Message permalinks

`tg personal messages link <chat> <message>` or `tg personal messages link <msg:locator>` returns
`{ item: { ref, url, access, reason } }` without message content. Channels/supergroups can have
public or restricted links; a link grants no membership. Dialogs, basic groups and Saved Messages
return only a locator. Offline validates the stored target, never connects and returns no URL.
Locators from another account are refused. This differs from graph `messages links`.
Read-only MCP offers `tg_read` (`command: "messages link"`) with the same result.

## Your own chat list and folders

Your own chat list: `chats archive|unarchive|pin|unpin|mark-unread <chat>` and `chats mute <chat> [--until 2h]` /
`unmute`. They change only your list and notifications; nobody in the chat is told. Repeating one is safe;
an unknown outcome is checked with `chats list`.

Folder rules: `chats folders create|update --include contacts,groups --skip muted,archived`.
On update these flags replace the previous rules; `none` clears them. Shared folders take no rules.
`--exclude-chat` excludes a chat and `--pin` puts it first. The returned emoji is the stored Telegram
folder icon; unsupported icons can be dropped. `folders order` returns only ids and titles.
`folders list` gives chat ids only; `folders show <folder>` (MCP `tg_read` with command `chats folders show`) names them.

## Forum topics

Forum setup uses `topics enable`: only the owner, explicit `--upgrade --yes` for a basic group,
whose chat id changes. Use the returned new id afterwards. `topics create` never enables topics
implicitly; never retry an unknown create; check `topics list`.
`topics create` and `topics edit` take `--emoji <emoji>` for the topic's icon, one of `topics icons list`;
`topics edit --emoji none` removes it.
`topics delete <chat> <id>` permanently deletes the topic and every message in it for everyone.
The General topic cannot be deleted. It asks first by default; use `--allow-dangerous` only when explicitly authorized.
An unknown outcome requires checking `topics list` before retrying.
An upgrade that succeeded before enable failed is retained; inspect the partial result and never
promise rollback to a basic group. Do not silently move old message locators to the new id.

## Invite links

For an extra invite link you own, `tg personal chats links update <chat> <link>` changes only explicitly supplied
`--approval` / `--no-approval`, `--expire-time <time>` or `--max-uses <n>` values. Supply at least
one change; it is a guarded write. Discover its current schema before changing a link.
MCP uses `tg_write` with command `chats links update`; do not reset a link to edit its settings.
