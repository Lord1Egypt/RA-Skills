# People: notes, aliases, tags, mentions and members

Read before a meeting or a reply to someone, to summarise or recommend a person, or for notes, aliases, chat tags, phones and links in messages, or group members.

- **Recommend a person:** compare actual evidence of relevant experience across chats. Match
  message sender IDs to `contacts show`, `contacts context` (what the store holds about one
  person, without connecting) and relevant personal chats; two identical display
  names are not one person. Past availability is not current availability. Prepare a draft
  unless the owner explicitly asks to send it to the identified recipient. If sending is
  refused by permissions, stop and keep the draft; do not change settings or switch profiles.

Local aliases belong to the selected account, notes show in every profile that sees the person;
both survive contact refresh, and never change messenger profiles or address-book names. `contacts rename` updates the messenger's
address book; use `contacts aliases` for a local name. Duplicate aliases require an explicit id.
Private notes are separate from the contact's public bio. Read/search them only when relevant.

Before the owner talks to someone (a call, a meeting, a reply), call `contacts prepare <person>`: context plus the
chats where they wrote last, their open tasks, accepted facts, notes and recent meetings, each with its reference,
from the store only; `prepare.coverage` says what was left out.
To summarise what one person said, call `contacts context <person> --chat <chat> --limit <n>` (MCP:
`chats` and `limit`); the answer is `{ at, text }` per message. Ask for `-v` (MCP `detail: 1`) only when
you need message ids or locators. Only `contacts context` without `--chat` gathers identities linked
with `contacts link`; `contacts show` and `--chat` read the named account only. `contacts show`
prints the whole phone number, as the other commands that show one; `--hide-phone` leaves it out.
`contacts check` sends the person's Telegram id to the public spam lists CAS and lols.bot; use
`--no-registries` (MCP `registries: false`) unless the owner accepts that. Its score is a hint, not a verdict.

```sh
echo "$PHONE" | tg personal contacts lookup --json   # a number through stdin, never as an argument
tg personal contacts aliases set 101 'Project lead'
tg personal contacts aliases remove 101
tg personal contacts notes add 101 --text-file /path/to/own-note.md
tg personal contacts notes list 101 --json
tg personal contacts notes show 101 NOTE_ID --json
tg personal contacts notes edit 101 NOTE_ID --revision 1 --text-file /path/to/own-note.md
tg personal contacts notes remove 101 NOTE_ID
tg personal contacts show 101 --with-notes --json
tg personal metadata show --chat CHAT_ID --json
tg personal metadata sync --chat CHAT_ID --limit 1 --json
tg personal tags rebuild --chat CHAT_ID --dry-run --json
tg personal tags rebuild --chat CHAT_ID --sync-first --limit 1 --json
tg personal tags list sources:auto --json
tg personal tags remove news --chat CHAT_ID --claim auto
```

Automatic tags use local keyword rules on cached group/channel titles, usernames and descriptions;
they do not use a model or message contents. Refresh is explicit and reads the messenger without
changing the chat. Dry-run uses cached data only and cannot be combined with refresh. Limit is
bounded at 500 chats. A rule score is not a probability. Automatic claims are separate from manual
labels; rerunning preserves manual labels. Without `--claim`, removing a label removes both claims.
A later explicit auto run can regenerate it. Linking identities never silently combines private notes.

Phones, e-mail addresses, links and Google documents written in stored messages are kept as mentions, found
by rules on every store write. `mentions list` takes a query: `kind:phone|email|url|document`,
`status:found|linked|dismissed`, `domain:` (a link's or address's site; `docs.google.com` means `google.com`)
and `value:`; a bare word is a value written any way, so `89001234567` finds `+79001234567`. Messages stored
before the store had mentions need one `mentions rebuild`. Text read from files (`attachments extract`) and voice
note transcripts yield mentions too (`field` `file_text` or `transcript`); attachments with text from before store
version 10 need one `mentions rebuild`. Each item has the message's `locator`; mention text goes to the owner only,
never into logs or files.

`mentions confirm <id> [person:<uid>|organization:<id>]` records who owns a phone or an address (a shop's number
belongs to the organization, apart from any person); `mentions reject <id>` dismisses a value for good.
`search messages` finds messages by mention: `phone:`, `email:` (`email:ana@example.com`), `url:`, `domain:`.

```sh
tg personal mentions list kind:phone --json
tg personal mentions list domain:google.com kind:url --json
tg personal mentions show 12 --json
tg personal mentions rebuild
tg personal mentions confirm 12 organization:3
tg personal search messages 'domain:docs.google.com'
```

Prepare for a meeting: find project groups and the participants' personal chats. A DM's
title need not contain the project name. Compare dated group messages with relevant DMs;
a later confirmation can close an old blocker. Use `messages evidence` for a brief, inspect
coverage and follow its cursor. Distinguish decisions, open questions and inferred dates.

## Group members

`tg personal chats members check <chat> --json` reads member pages with reasons; it removes nobody.
Treat scores as hints; check `more` and `unknown`, and review each person before any moderation action.

Telegram maps member flags, photos and join/inviter metadata when present; inspect unknown signals.
