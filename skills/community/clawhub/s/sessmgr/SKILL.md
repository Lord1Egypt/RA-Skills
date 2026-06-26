---
name: sessmgr
description: Name, list, reload, rename, save, delete sessions. /sessmgr <action>. Nat: "name session".
metadata:
  {"openclaw": {"emoji": "🔖"}}
---

# Sessmgr — Named Session Manager

Give your OpenClaw sessions memorable names and pick them up exactly where you left off. No more hunting through cryptic session IDs.

## At a Glance

```
/sessmgr <action> [args]

Actions:
  name     <name> [description]    Name the current session
  list                           Show all named sessions
  reload   <name>                 Switch to a named session
  new      <name>                 Start a fresh named session
  rename   <old> <new>            Rename a session
  save     <name>                 Touch a session's last-used time
  delete   <name>                 Remove a name (keeps transcript)
```

**Natural language works too** — "name this session project-alpha", "switch to my-dev-session", etc.

---

## Why Named Sessions?

- **Remember what you were doing** — "auth-redesign" beats `199f3a3c-882a-4cec-9f86-693bca7b9fa1`
- **Pick up exactly where you left off** — `/sessmgr reload project-alpha` restores context
- **Multiple concurrent threads** — name each conversation thread, switch between them instantly
- **Never lose context** — deleting a name preserves the transcript; you can always recover

---

## Actions

### `name <name> [description]`
**What it does:** Tags the current session with a memorable name.

```
/sessmgr name auth-redesign OAuth flow refactor
```

**Natural language:** *"name this session auth-redesign"* / *"call this session my blog draft"*

**Details:**
- If the name already belongs to this session → updates the description
- If the name belongs to a different session → error (use `rename` to reclaim it)
- Description is optional but recommended — "OAuth flow refactor" beats nothing

**Output on success:**
```
Named session 'auth-redesign' -> 199f3a3c-882a-4cec-9f86-693bca7b9fa1
  Description: OAuth flow refactor
```

---

### `list`
**What it does:** Shows all named sessions with metadata.

```
/sessmgr list
```

**Natural language:** *"list my sessions"* / *"show all named sessions"*

**Output:**
```
Name              Session ID                        Created                     Last Used                   Description
--------------------------------------------------------------------------------------------------------------------------------------
auth-redesign     199f3a3c-882a-4cec-9f86-693bca7b9fa1  2026-04-19T11:08:49+00:00   2026-04-19T14:22:00+00:00   OAuth flow refactor
dev-work          a1b2c3d4-e5f6-7890-abcd-ef1234567890  2026-04-18T09:30:00+00:00   2026-04-18T16:45:00+00:00   Backend API investigation
```

**Tips:**
- Active session is marked implicitly by having the most recent `lastUsed` that matches your current session ID
- Sessions are sorted alphabetically

---

### `reload <name>`
**What it does:** Switches to a named session by printing `RELOAD_SESSION:<sessionId>`.

```
/sessmgr reload auth-redesign
```

**Natural language:** *"switch to auth-redesign"* / *"go to session dev-work"* / *"load project-alpha"*

**Output on success:**
```
RELOAD_SESSION:199f3a3c-882a-4cec-9f86-693bca7b9fa1
```

**If the name doesn't exist:**
```
Error: no session named 'auth-redesign'. To start a new session with this name, use /sessmgr new auth-redesign
```

> ⚠️ **Channel limitation:** Reloading only works within the same channel. Webchat sessions reload in webchat, Telegram in Telegram, etc. Cross-channel switching is not supported.

---

### `new <name>`
**What it does:** Confirms the name is available, then prints `NEW_SESSION:<name>` to signal intent to start fresh.

```
/sessmgr new project-alpha
```

**Natural language:** *"start a new session called project-alpha"* / *"create a new session named staging"*

**Output on success:**
```
NEW_SESSION:project-alpha
```

**If the name already exists:**
```
Error: a session named 'project-alpha' already exists. Use /sessmgr reload project-alpha to return to it.
```

---

### `rename <old-name> <new-name>`
**What it does:** Changes the name of an existing session without touching the transcript.

```
/sessmgr rename dev-work backend-research
```

**Natural language:** *"rename dev to staging"* / *"change session name from old-session to new-session"*

**Output on success:**
```
Renamed 'dev-work' -> 'backend-research'.
```

**Validation:**
- `new-name` must be unique (no existing session with that name)
- Both names must be valid: letters, numbers, hyphens, underscores only
- Transcript file is never modified — only the name mapping changes

---

### `save <name>`
**What it does:** Updates the `lastUsed` timestamp without leaving the current session. Useful for marking a session as "alive" without switching.

```
/sessmgr save auth-redesign
```

**Natural language:** *"save session auth-redesign"* / *"touch the timestamp for my dev session"*

**Output:**
```
Saved session 'auth-redesign' (updated lastUsed).
```

---

### `delete <name>`
**What it does:** Removes the name mapping. The transcript file (`.jsonl`) is **never deleted** — only the human-readable name is removed.

```
/sessmgr delete old-session
```

**Natural language:** *"delete session old-session"* / *"remove the name old-session"*

**Output:**
```
Deleted session name 'old-session' (session file preserved).
```

**Recovery:** If you delete a name by accident, the session transcript still exists at `~/.openclaw/agents/main/sessions/<sessionId>.jsonl`. You can find it by checking `sessions.json` and re-name it with `/sessmgr name`.

---

## Data Storage

| File | Purpose |
|------|---------|
| `~/.openclaw/agents/main/sessions/names.json` | Name → sessionId mapping with metadata |
| `~/.openclaw/agents/main/sessions/<sessionId>.jsonl` | The actual session transcript (never deleted) |

**names.json entry structure:**
```json
{
  "sessionId": "199f3a3c-882a-4cec-9f86-693bca7b9fa1",
  "created": "2026-04-19T11:08:49.440540+00:00",
  "lastUsed": "2026-04-19T14:22:00.000000+00:00",
  "description": "OAuth flow refactor"
}
```

---

## Validation Rules

| Rule | Details |
|------|---------|
| Allowed characters | Letters (`a-z`, `A-Z`), digits (`0-9`), hyphens (`-`), underscores (`_`) |
| Max length | 64 characters |
| Case | Preserved — `Auth-Redesign` and `auth-redesign` are different names |
| Reserved names | None, but avoid names that look like actions (`name`, `list`, `new`, etc.) to prevent ambiguity |

---

## Error Reference

| Situation | Message |
|-----------|---------|
| Name doesn't exist (reload) | `Error: no session named '<name>'. To start a new session with this name, use /sessmgr new <name>` |
| Name already taken (new) | `Error: a session named '<name>' already exists. Use /sessmgr reload <name> to return to it.` |
| Name belongs to another session | `Error: name '<name>' is already assigned to a different session.` |
| Invalid characters | `Error: name must be alphanumeric, hyphens, or underscores only.` |
| Can't determine current session | `Error: could not determine current session ID.` |
| New name already exists (rename) | `Error: name '<new-name>' already exists.` |
| Name doesn't exist (save/delete/rename) | `Error: no session named '<name>'.` |

---

## Tips & Tricks

**Multiple projects simultaneously:**
```
/sessmgr name frontend-rework
# work on frontend...
/sessmgr name backend-api  
# work on backend...
/sessmgr reload frontend-rework  # pick up exactly where you left off
```

**Meaningful descriptions:**
```
/sessmgr name auth-redesign "Fixing OAuth callback, third attempt"
```

**Check before starting new:**
```
/sessmgr list
# see if 'staging' already exists before /sessmgr new staging
```

**Session cleanup without losing history:**
```
/sessmgr delete old-session  # removes the name
# transcript still at: ~/.openclaw/agents/main/sessions/<sessionId>.jsonl
```
