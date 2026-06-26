# Session Rename

Assigns a custom title to a session or checks the current name.

## Mechanism

Claude Code stores custom titles by appending the following record to the session JSONL file:

```json
{"type":"custom-title","customTitle":"<title>","sessionId":"<uuid>"}
```

## Script Usage

> ⚠️ **Full UUID required** — Short 8-character IDs (`99f1f311`) do not work. Always use the full UUID (`99f1f311-8c3d-43ba-b212-e3184965fed4`).

```bash
SCRIPT=~/.claude/skills/session/scripts/rename-session.sh

# Assign a name to a specific session
bash "$SCRIPT" 99f1f311-8c3d-43ba-b212-e3184965fed4 "Authentik SSO OIDC Integration"

# Assign a name to the latest session in the current project
bash "$SCRIPT" "session name"

# Check current title
bash "$SCRIPT" --show 99f1f311-8c3d-43ba-b212-e3184965fed4

# List named sessions in the current project
bash "$SCRIPT" --list
```

## Running Directly from Claude Code

Procedure for Claude to identify session content via AI and assign an appropriate name:

1. Extract user messages from the session file to understand the content
2. Generate a short title summarizing the key tasks
3. Append a custom-title record to the JSONL using `rename-session.sh`

### Python Priority When Parsing JSONL

When parsing JSONL to understand session content, try in the following order:

```bash
# 1st priority: python3
head -c 3000 <session.jsonl> | python3 -c "..."

# 2nd priority: python
head -c 3000 <session.jsonl> | python -c "..."

# 3rd priority: uv (when both python/python3 are unavailable)
head -c 3000 <session.jsonl> | uvx python -c "..."

# 4th priority: node (when uv is also unavailable)
head -c 3000 <session.jsonl> | node -e "..."
```

On Windows, python3/python may not be available, so fall back in the order: uv → node.

## Naming Guide

- **Length**: 20–40 characters recommended
- **Format**: `<topic> - <key task>` (e.g., `Authentik SSO OIDC Integration - dt login/logout`)
- **Language**: English preferred; technical terms in English
- **Avoid**: Dates, and unnecessary words like "session" or "task"

## Quick Naming (Claude Instruction)

```
/session <session_id> assign an appropriate name to this session
```

Claude will read the session content and automatically suggest and apply a name.
