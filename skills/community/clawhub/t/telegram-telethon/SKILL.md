---
name: telegram-telethon
description: Manage Telegram via tgctl-telethon CLI (Python/Telethon) - send/forward/edit/delete/pin messages, search, list chats/members, join/leave groups, kick/invite users, block/unblock, send files, download media, start bots, create groups/channels, manage admins, update profile, listen for messages. Use when user asks to interact with Telegram as a user account (not bot API). Powered by Telethon (MTProto).
---

# Telegram CLI (tgctl-telethon)

User-account-level Telegram management via Python + Telethon. Drop-in replacement for the Go-based tgctl with the same CLI interface.

## First-Time Setup

### Step 1: Install

```bash
bash <skill-dir>/scripts/install.sh
```

This installs `telethon` via pip and copies `tgctl-telethon` to `~/.local/bin/`.

### Step 2: Get API credentials

Ask the user to go to https://my.telegram.org → API Development → get `api_id` and `api_hash`.

### Step 3: Login

```bash
TELEGRAM_API_ID=${ID} TELEGRAM_API_HASH=${HASH} tgctl-telethon login
```

User enters phone number, auth code (digits only, no spaces), and optional 2FA password interactively.

**Important:** Auth codes must NOT be sent via Telegram (will be invalidated).

### Step 4: Save config to TOOLS.md

```markdown
### tgctl-telethon (Telegram CLI)
- Binary: ~/.local/bin/tgctl-telethon
- Env: TELEGRAM_API_ID=${ID} TELEGRAM_API_HASH=${HASH}
- Session: ~/.tgctl-telethon/
```

## Prerequisites

- Python 3.9+
- `telethon` pip package
- `TELEGRAM_API_ID` and `TELEGRAM_API_HASH` env vars
- Session persists in `~/.tgctl-telethon/<profile>/`

## Commands

```bash
TELEGRAM_API_ID=${ID} TELEGRAM_API_HASH=${HASH} tgctl-telethon [--profile <name>] <command>
```

### Messaging

| Command | Description |
|---------|-------------|
| `send <chat> <msg>` | Send message |
| `forward <from> <to> <msg_id>` | Forward a message |
| `edit <chat> <msg_id> <text>` | Edit a message |
| `delete <chat> <msg_id>` | Delete a message |
| `pin <chat> <msg_id>` | Pin a message |
| `unpin <chat> [msg_id]` | Unpin message (or all) |
| `read <chat>` | Mark chat as read |
| `sendfile <chat> <file> [--caption text]` | Send file or image |
| `download <chat> <msg_id> [-o path]` | Download media |
| `callback <chat> <msg_id> <data>` | Click inline button |
| `typing <chat>` | Send typing status |

### Search & Browse

| Command | Description |
|---------|-------------|
| `chats [limit]` | List chats |
| `history <chat> [limit]` | Chat history |
| `search <query>` | Search chats and users |
| `search-msg <chat> <query> [--limit N]` | Search messages in chat |
| `contacts` | List contacts |
| `members <chat> [limit]` | List group/channel members |
| `chatinfo <chat>` | Get chat/user details |
| `resolve <username>` | Resolve username to ID |
| `resolvephone <phone>` | Resolve phone to user |

### Group & Channel Management

| Command | Description |
|---------|-------------|
| `creategroup <title> <user1> [user2...]` | Create a group |
| `createchannel <title> [about]` | Create a channel |
| `join <link_or_username>` | Join group/channel |
| `leave <chat>` | Leave group/channel |
| `kick <chat> <user>` | Kick user |
| `invite <chat> <user>` | Invite user |
| `editadmin <chat> <user> [--remove]` | Set/remove admin |
| `startbot <chat> <bot> [param]` | Start bot in chat |

### User & Account

| Command | Description |
|---------|-------------|
| `login` | Login (phone + code + optional 2FA) |
| `me` | Current user info |
| `updateprofile [--first n] [--last n] [--about t]` | Update profile |
| `setstatus <online\|offline>` | Set online status |
| `block <user>` | Block user |
| `unblock <user>` | Unblock user |
| `listen [--user id] [--chat id]` | Listen for messages |
| `logout` | Logout |

## Multi-Account (--profile)

```bash
tgctl-telethon --profile work login
tgctl-telethon --profile work me
```

Sessions stored in `~/.tgctl-telethon/<profile>/`.

## Chat ID Format

- **User**: Positive ID (e.g. `8568316820`)
- **Group/Channel**: Negative ID (e.g. `-3842028710`)
- **@username**: Use directly (e.g. `@BotFather`)

## Security

- All credentials via environment variables, never stored in code
- Session files stored locally in `~/.tgctl-telethon/`, never transmitted
- Login requires interactive user input
- Auth codes must NOT be sent via Telegram
- Communicates only with official Telegram servers
