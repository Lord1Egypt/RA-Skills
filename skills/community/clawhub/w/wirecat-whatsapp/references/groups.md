# Groups, communities, channels, contacts and the account

## Groups

- **Group changes are writes the members see**, and go through the profile's permissions like a send.
- `chats create` and `members add` refuse anyone the owner never wrote to and has not saved — WhatsApp bans accounts
  that add strangers; never work round it.
- Group admin: `chats create|join|leave|update`, a group photo by `chats update --photo` (a square JPEG of 190 to 720
  pixels a side) or `--remove-photo`, `chats links show|reset`, `chats members list|fetch|add|remove`,
  `chats admins add|remove`, `chats requests list|confirm|reject`.
- `admins add` takes no `--can`: a WhatsApp admin has every right.
- `chats update --disappear-after` takes 24h, 7d, 90d or off, nothing else.
- A chat or person named by name is looked up in the store first (part of the name is enough; several matches are
  refused), then in WhatsApp's chat list; a group the store does not hold yet needs its `…@g.us` id.
- `chats show` answers from the store; `chats members list` asks WhatsApp, and with `--offline` shows the stored
  members.
- `chats events` and `chats members history` answer from the store ([history](history.md)).
- `chats delete|clear` ask first in a terminal. `metadata sync` fetches a group's title and description, for
  `tags rebuild`.
- WhatsApp has no `chats folders`, no `messages comments`, no second invite link, no partial admin rights and no
  account age (a `newAccount` rule in `chats rules set` is refused).

## Communities

A group in a WhatsApp community names it in `parent_chat_id`, and the community itself is a group with
`provider_metadata.community: true`, in the store (`chats list`, `chats show`) and in the answers of
`chats create|join|update`. Listing a community's groups or linking one is not built yet.

## Channels

A channel (`…@newsletter`) is followed with `chats join <whatsapp.com/channel link>` and left with `chats leave`;
`messages sync <channel>` reads its posts from WhatsApp's servers, and every post's sender is the channel.
`messages send <channel> <text>` posts, with one file (`--photo`, `--file`, `--voice`) or none, only where the owner
is the channel's owner or an admin (else exit 5), and every follower sees it at once: no reply, album, poll, forward,
edit or deletion in a channel. `chats create --channel` is not built yet.

## Contacts

- `contacts show|block|unblock|lookup|sync|add|rename` work; `contacts remove|import` are refused.
- `contacts add|rename` write a WhatsApp contact name, on every device of the account, with nothing sent to the
  person; for someone saved in the phone's Contacts app the phone keeps that app's name, and the account's own number
  is refused.
- `contacts lookup` takes one number on stdin, at most one every 10 seconds per profile; never loop it.
- `contacts list`, `contacts show`, `contacts context` and `stats chats show` are marked as reading from WhatsApp: add
  `--offline` to keep them on the store.

## The account

- `account update` sets the name, the about text and a square JPEG photo.
- `account privacy show|set`: `set` has WhatsApp's settings only (last seen, online, photo, about, read receipts,
  groups, calls); `--read-receipts off` also stops the owner seeing others' receipts, and `contacts_except` is shown,
  never set.
- `account sessions` is not built yet.

```sh
wa personal chats members list 120363000000000001@g.us --json  # who is in the group now; connects
```
