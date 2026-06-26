# 🔖 Sessmgr — Named Session Manager

<div align="center">

**Give your OpenClaw sessions memorable names — then pick them up exactly where you left off.**

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://clawhub.ai)
[![Python](https://img.shields.io/badge/Python-3-green)](https://python.org)

_Rename, switch, save, and organize your sessions without losing context._

</div>

---

## ✨ What It Does

| Feature | Description |
|---------|-------------|
| 🔖 **Name sessions** | Tag sessions with memorable names like `auth-redesign` or `blog-draft` |
| 📋 **Rich metadata** | Stores created date, last-used, and description per session |
| 🔄 **Instant switching** | Jump to any named session — no hunting through session IDs |
| ✏️ **Rename anytime** | Change a session's name without losing its transcript |
| 💾 **Save snapshots** | Update `lastUsed` timestamp without leaving the current session |
| 🗑️ **Safe delete** | Remove only the name — transcript is always preserved |
| 🌐 **Natural language** | Works with both slash commands and plain English |

---

## 🚀 Quick Start

All operations go through **`/sessmgr`** with an action sub-command:

```
/sessmgr <action> [args]
```

### Name the current session

```
/sessmgr name auth-redesign OAuth callback fix
```

_or just say:_ "name this session auth-redesign"

### List all named sessions

```
/sessmgr list
```

```
Name              Session ID                        Created                     Last Used                   Description
-------------------------------------------------------------------------------------------------------------------------------------
auth-redesign     199f3a3c-882a-4cec-9f86-693bca7b9fa1  2026-04-19T11:08:49+00:00   2026-04-19T14:22:00+00:00   OAuth callback fix
dev-work          a1b2c3d4-e5f6-7890-abcd-ef1234567890  2026-04-18T09:30:00+00:00   2026-04-18T16:45:00+00:00   Backend API investigation
```

### Switch to a named session

```
/sessmgr reload auth-redesign
```

_or just say:_ "switch to auth-redesign"

### Start a fresh named session

```
/sessmgr new staging-env
```

_(If `staging-env` already exists, you'll get an error telling you to use `/sessmgr reload` instead.)_

### Rename a session

```
/sessmgr rename dev-work backend-research
```

### Save (mark as active without switching)

```
/sessmgr save auth-redesign
```

### Delete a session name

```
/sessmgr delete old-session
```

_(The transcript is preserved — only the name mapping is removed.)_

---

## 📖 Action Reference

| Action | Slash Command | Natural Language |
|--------|--------------|------------------|
| **Name current session** | `/sessmgr name <name> [description]` | "name this session \<name\>" |
| **List all sessions** | `/sessmgr list` | "list my sessions" |
| **Reload by name** | `/sessmgr reload <name>` | "switch to session \<name\>" |
| **Start new named session** | `/sessmgr new <name>` | "start new session called \<name\>" |
| **Rename a session** | `/sessmgr rename <old> <new>` | "rename session \<old\> to \<new\>" |
| **Save (touch timestamp)** | `/sessmgr save <name>` | "save session \<name\>" |
| **Delete name only** | `/sessmgr delete <name>` | "delete session \<name\>" |

---

## 💡 Use Cases

### Multi-project switching

```
/sessmgr name frontend-rework
# work on frontend for a while...
/sessmgr name backend-api
# work on backend...
/sessmgr reload frontend-rework  # jump back, context intact
```

### Meaningful session descriptions

```
/sessmgr name auth-redesign "Third attempt at fixing OAuth callback"
```

### Check before creating

```
/sessmgr list  # is 'staging' already taken?
/sessmgr new staging-env
```

### Safe cleanup

```
/sessmgr delete old-session  # removes name only
# transcript still at: ~/.openclaw/agents/main/sessions/<sessionId>.jsonl
```

---

## 📁 Data Storage

Session names are stored in:

```
~/.openclaw/agents/main/sessions/names.json
```

Each entry contains:

```json
{
  "sessionId": "199f3a3c-882a-4cec-9f86-693bca7b9fa1",
  "created": "2026-04-19T11:08:49.440540+00:00",
  "lastUsed": "2026-04-19T14:22:00.000000+00:00",
  "description": "OAuth callback fix"
}
```

> **Note:** The actual session transcript (`.jsonl` file) is **never deleted** — only the name mapping is removed when you delete a session name.

---

## ⚙️ Requirements

- Python 3
- OpenClaw session store at `~/.openclaw/agents/main/sessions/`
- No external dependencies — pure stdlib Python
- **`OPENCLAW_SESSION_ID`** environment variable (set automatically by OpenClaw — no config needed)

---

## 🔧 Installation

Install via ClawHub:

```bash
clawhub install sessmgr
```

Or manually copy `sessmgr/` into:

```
~/.openclaw/workspace/skills/sessmgr/
```

Restart the gateway or start a new session.

---

## 🛡️ Security Notes

- Session names are stored locally only — no data leaves your machine
- Deleting a session name does **not** delete the transcript file
- The skill reads `OPENCLAW_SESSION_ID` from the environment to identify the current session
