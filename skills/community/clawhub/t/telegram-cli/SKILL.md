---
name: node-telegram-cli
description: CLI tool for Telegram via MTProto. Send/read messages, manage groups, search conversations, download media, and automate Telegram workflows. Use when the task involves any Telegram account interaction.
---

### Source & Trust

1. Repository: https://github.com/baontq23/node-telegram-cli
2. npm: https://www.npmjs.com/package/node-telegram-cli (published with provenance)
3. Credentials are stored securely via OS Keychain (macOS Keychain / Windows Credential Manager / Linux Secret Service), not in plaintext files

### Installation

1. Requires Node.js >= 20
2. Install globally: `npm install -g node-telegram-cli`
3. Verify: `ntg --version`
4. Run `ntg login` once — interactive, requires phone number + OTP code from Telegram

### Critical Rule: Always Use JSON Mode

1. Add `--json` flag to every command for machine-readable output
2. `--json` is a global flag — place it before or after the subcommand
3. Example: `ntg --json inbox`, `ntg --json search @user "keyword"`

### Peer Format

1. `@username` — most reliable, e.g. `@johndoe`
2. Phone number — for contacts without username, e.g. `+84901234567`
3. `me` — your own Saved Messages
4. Chat title — group/channel name in quotes, e.g. `"My Group"`

### Read Commands (No Side Effects)

1. `ntg --json inbox` — list recent conversations
2. `ntg --json inbox --unread` — only unread conversations
3. `ntg --json inbox --private` — only private 1-on-1 chats
4. `ntg --json inbox --unread --private` — combine filters
5. `ntg --json inbox --chat <peer> --limit <n>` — messages from a specific chat
6. `ntg --json search <peer> "keyword"` — search in a specific chat
7. `ntg --json global-search "keyword"` — search across all chats
8. `ntg --json chat-info <chat>` — show group/channel info

### Write Commands (Has Side Effects)

1. `ntg msg <peer> "text"` — send a text message
2. `ntg msg <peer> "text" --silent` — send silently (no notification sound)
3. `ntg fwd <user> <msgId>` — forward a message by ID
4. `ntg mark-read <peer>` — mark all messages as read
5. `ntg delete-msg <msgId>` — delete a message
6. `ntg send-photo <peer> <file>` — send a photo
7. `ntg send-video <peer> <file>` — send a video
8. `ntg send-file <peer> <file>` — send a text file as plain messages
9. `ntg download <msgId> --chat <peer>` — download media from a message
10. `ntg download <msgId> --chat <peer> --type <type>` — specify media type (photo, video, audio, doc)
11. `ntg view <msgId> --chat <peer>` — download and open with system viewer
12. `ntg clean-downloads` — delete all downloaded media files

### Group Management

1. `ntg create-group "Topic" @user1 @user2` — create a new group
2. `ntg chat-add <chat> <user>` — add a user to a group
3. `ntg chat-kick <chat> <user>` — remove a user from a group
4. `ntg chat-rename <chat> "New Name"` — rename a group
5. `ntg chat-set-photo <chat> <file>` — set group photo

### Contact Management

1. `ntg add-contact <phone> <firstName> <lastName>` — add a contact
2. `ntg rename-contact <user> <firstName> <lastName>` — rename a contact

### JSON Output Schemas

#### Inbox (conversation list)

1. `name` — contact/chat display name
2. `peer` — identifier to use as `<peer>` argument
3. `peerType` — "username" | "phone" | "id"
4. `type` — "user" | "group" | "channel"
5. `unreadCount` — number of unread messages
6. `lastMessage` — text/caption (empty string if media-only)
7. `lastMessageId` — use with `ntg download <id>` for media
8. `mediaType` — "photo" | "video" | "document" | "audio" | "voice" | "sticker" | "location" | "contact" | "poll" | null
9. `date` — ISO 8601 timestamp

#### Chat messages (inbox --chat)

1. `id` — message ID
2. `date` — ISO 8601 timestamp
3. `sender` — sender display name
4. `text` — message text/caption
5. `mediaType` — same values as above
6. `isOutgoing` — true if sent by you

### Error Handling

1. Exit code `0` = success
2. Exit code `1` = error (not logged in, peer not found, etc.)
3. If not logged in, commands fail with: "Not logged in. Run ntg login first."

### Important Notes

1. Do NOT use `ntg chat <peer>` — it is interactive, blocks stdin, not suitable for automation
2. Session persists until `ntg logout` is called — no re-login needed between commands
3. Downloaded files are saved to `~/.telegram-cli/downloads/`
4. Always specify `--chat <peer>` when downloading media to identify the source chat
