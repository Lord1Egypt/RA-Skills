# Session Rename

Suggests and applies a name to a session.

## Procedure

### 0. Check Whether a Name Was Specified

- If the user specified a name directly → **skip to step 2** (skip suggestions)
- If no name was specified (e.g. `/session rename`, `/session name`, `suggest a name`) → **start from step 1**

> ⚠️ A topic alias such as the literal word `name` in `/session name` is **not** a title — treat it as "no name specified" and start from step 1.

### 1. Generate Name Candidates

Analyze the conversation content and generate 2–4 name candidates.

**Naming rules:**
- **Length**: 20–40 characters recommended
- **Format**: `<topic> + <key action>` (e.g. `feat/76-auth-history + SSO deployment validation`)
- **Language**: English preferred; technical terms in English
- **Avoid**: dates, unnecessary words like "session" or "task"

### 2. Apply the Name

**Current session** → Output as copyable list only (NO AskUserQuestion):

```
Session name suggestions:

1. `/rename Candidate 1`
2. `/rename Candidate 2`
3. `/rename Candidate 3`
```

`/rename` is a Claude Code built-in command — cannot be invoked via Bash or Skill tool.
The user copies and pastes the desired `/rename ...` line.

| # | Don't | Do |
|---|-------|-----|
| 1 | Call `rename-session.sh <current-id> "title"` for the current session | Output the copyable `/rename` list and let the user apply it |
| 2 | Trust the SessionStart hint (`To rename this session: bash ...rename-session.sh`) as the current-session method | The hook hint is for **other**-session tooling. Current session = `/rename` built-in only |
| 3 | Pick and apply a title yourself for the current session | Suggest 2–4 candidates; the user chooses via `/rename` |

The script (`rename-session.sh`) appends `custom-title`/`agent-name` records, which is correct only for a **different** session's JSONL — for the live current session, the built-in `/rename` is the supported path.

**Other session** (session ID specified) → AskUserQuestion to select, then apply via script:

```
AskUserQuestion {
  question: "Select a session name",
  header: "Session Name",
  options: [
    { label: "Candidate 1" },
    { label: "Candidate 2" },
    { label: "Candidate 3" }
  ]
}
```

Then rename via script:

```bash
scripts/rename-session.sh <session_id> "<selected name>"

# Check current title
scripts/rename-session.sh --show <session_id>

# List named sessions
scripts/rename-session.sh --list
```

## Storage Format

Both records are appended together at the end of the session JSONL:

```json
{"type":"custom-title","customTitle":"<title>","sessionId":"<uuid>"}
{"type":"agent-name","agentName":"<title>","sessionId":"<uuid>"}
```

`custom-title` is displayed as the GUI title, and `agent-name` is displayed as the agent name in the session list.
