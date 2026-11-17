# Sending, editing, deleting, reacting

Most commands here write to WhatsApp and connect (through `serve` when it runs, see [connection](connection.md)).
The boundaries in SKILL.md hold for each one: only what the owner asked for, in the chat the owner named.

## Before a write

- **Send nothing the owner did not ask for.** `wa personal messages send` (also with `--reply-to`),
  `messages edit`, `messages delete`, `wa personal reactions add` and `wa personal polls create|vote` only when the
  owner asked for this exact text, emoji, poll or answer in this exact chat. A draft, "we should probably answer", a
  conclusion drawn from what you read — none of these is a request.
- **Never send to a number the owner has not written to before, and never in bulk.** WhatsApp bans accounts for
  both. No loops over chats, no "send this to everyone in the group". A number the owner has not been in touch with
  only when the owner names it in this request, and never several such numbers at once.
- **Delete only the exact messages the owner named, and never add `--for-everyone`, `--allow-dangerous` or `--yes`
  on your own.** A deletion cannot be undone; the flags are the owner's word. `messages delete` alone is for the owner
  only. An agent never deletes for everyone: `--for-everyone` is for the owner to run himself.
- A chat or person named by name is looked up in the store first (part of the name is enough; several matches are
  refused), then in WhatsApp's chat list; a group the store does not hold yet needs its `…@g.us` id.
- A post to a channel (`…@newsletter`) reaches every follower at once, and only the channel's owner or an admin may
  post: see [groups](groups.md#channels).
- Global `--dry-run` checks syntax and permissions before a sensitive write; it opens no connection, reserves no write
  and leaves targets unresolved.
- **`--offline` answers from the local store** and never connects. A send with `--offline` is always refused.

## How WhatsApp takes a write

- **A change to a message needs it in the store.** WhatsApp addresses a message by its id *and* its sender, so
  `messages edit`, `messages delete`, `messages star|unstar`, `reactions add|remove`, `polls show|vote|voters` and
  `chats mark-read` look the message up in the store. One the store lacks is exit `6`.
- `messages download`, `messages forward` and `messages transcribe --local` work the same way, from the file keys the
  store holds; a file WhatsApp no longer keeps is asked of the owner's phone again, which must be online (a `timeout`
  otherwise); so far the phone's new copy cannot be read, so expect `media.retry-failed` and tell the owner the file
  is too old for `wa`.
- A `--reply-to` a message the store lacks still sends, but the phone may show the quote as unavailable.
- **An edit works only on the owner's own message, within 20 minutes of sending.**
- **`--md`** on a send or an edit writes Markdown as WhatsApp's marks (`*bold*`, `_italic_`, `~strike~`, code,
  quotes); underline and spoilers become plain text.
- **One file per message, or an album.** `messages send --file|--photo|--voice` sends one; the text is its caption, a
  voice note goes alone. `--photo` with a video `--file` goes as one album; a document cannot join one. Two files on a
  send go as an album only when both are photos or videos.
- WhatsApp has no silent, scheduled or send-as delivery, so there is no `--silent`, `--at-time` or `--send-as`.
- **Multi-line text goes through stdin only.** Leave out the last argument and the text is read from input:
  `printf 'first\n\nthird' | wa personal messages send 100000000000001@lid`.
- **Polls.** A WhatsApp poll never closes and every vote can change, so there is no `polls close` and no `--revote`.
  Counts are what the store heard ([history](history.md)).
- `messages pin|unpin`: every pin tells the chat; `--expire-time 24h|7d|30d`.
- `chats mark-read` clears the unread mark up to the chosen message and sends a read receipt the other side sees:
  only when the owner asked.

## After a write

- **Exit `14` means an unknown write outcome, not permission to replay it** (also when the engine stopped during
  it). Look in `wa personal sends list --json` and the chat's stored messages first. Repeat a send only with the same
  chat, text and `--operation-id`; never repeat an unknown write on the strength of its error code alone.
- **A refusal with exit code `5`, `7` or `8` on a change is the owner's decision, not a fault.** Do not work around
  it: do not change settings, do not call `wa personal recipients add`, do not wait and retry. Tell the owner the
  send did not go, and why. `account.rate-limited` (exit `8`) holds every write, reactions and read receipts too, for
  15 minutes.

## Recipes

The ids are made up — use the real ones from the previous answer.

```sh
wa personal messages send 100000000000001@lid "On my way" --json               # only when asked; connects
wa personal messages send 120363000000000001@g.us "Yes" --reply-to 3EB0A1B2C3D4E5F6A7B8 --json
wa personal messages edit 100000000000001@lid 3EB0A1B2C3D4E5F6A7B8 "On my way, 10 min" --json  # own, within 20 min
wa personal reactions add 100000000000001@lid 3EB0A1B2C3D4E5F6A7B8 👍 --json
wa personal chats mark-read 100000000000001@lid    # the other side sees it: only when asked
```
