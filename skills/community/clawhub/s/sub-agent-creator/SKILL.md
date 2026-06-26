---
name: agent-creator
description: "Full workflow for creating an OpenClaw Agent. Use when the user says 'create an agent', 'make a new agent', 'add a bot', or needs to set up a new AI assistant. Covers the complete setup process including (1) adding agent config and peer bindings to openclaw.json, (2) creating workspace directory with SOUL.md persona, (3) scaffolding required folders and files, (4) copying agent runtime configs from main, (5) restarting gateway to apply changes."
---

# Agent Creator - OpenClaw Agent Setup Tool

Automates the full end-to-end flow for creating an OpenClaw Agent.

## Trigger Phrases

Activate when user says things like:
- "Create an agent"
- "Make a new bot"
- "Set up a new agent"
- "Add an AI assistant"

## Full Workflow

### Step 1: Gather Information

Ask the user:
1. **Agent ID** (lowercase, hyphens only): e.g. `qisi`, `code-review`, `brainstorm`
2. **Agent Display Name**: e.g. "Brainstorm Buddy", "Code Reviewer"
3. **Purpose / Personality**: What does this agent do? What's its style?
4. **Group Chat Binding** (optional): peer.id of a group chat, e.g. `oc_xxx` (kind = group)
5. **Direct Chat Binding** (optional): peer.id of a user, e.g. `ou_xxx` (kind = direct)

### Step 2: Create Workspace Directory

```bash
OPENCLAW_DIR=~/.openclaw
mkdir -p $OPENCLAW_DIR/workspace-{agent_id}
mkdir -p $OPENCLAW_DIR/workspace-{agent_id}/memory
mkdir -p $OPENCLAW_DIR/workspace-{agent_id}/skills
```

### Step 3: Write Workspace Files

Create the following files in the workspace directory:
- `SOUL.md` — Agent persona (see template below)
- `USER.md` — User info template
- `AGENTS.md` — Session bootstrap instructions
- `HEARTBEAT.md` — Heartbeat config
- `TOOLS.md` — Tool notes
- `memory/` — Daily memory folder
- `IDENTITY.md` — Agent identity definition (optional)
- `BOOTSTRAP.md` — First-run bootstrap (optional)

**AGENTS.md content** (copied from ~/.openclaw/workspace/AGENTS.md):
```markdown
# AGENTS.md - Your Workspace

If `BOOTSTRAP.md` exists, that's your birth certificate. Follow it, figure out who you are, then delete it.

## Every Session

Before doing anything else:

1. Read `SOUL.md` — this is who you are
2. Read `USER.md` — this is who you're helping
3. Read `memory/YYYY-MM-DD.md` (today + yesterday) for recent context
4. **If in MAIN SESSION** (direct chat with your human): Also read `MEMORY.md`

## Memory

You wake up fresh each session. These files are your continuity:

- **Daily notes:** `memory/YYYY-MM-DD.md` — raw logs of what happened
- **Long-term:** `MEMORY.md` — your curated memories

## Safety

- Don't exfiltrate private data
- When in doubt, ask.
```

**HEARTBEAT.md content**:
```markdown
# HEARTBEAT.md

# Keep this file empty to skip heartbeat API calls.
```

**TOOLS.md content**:
```markdown
# TOOLS.md - Local Notes

Notes specific to this agent's setup.
```

### Step 4: Create Agent Runtime Directory

```bash
OPENCLAW_DIR=~/.openclaw
mkdir -p $OPENCLAW_DIR/agents/{agent_id}/agent
mkdir -p $OPENCLAW_DIR/agents/{agent_id}/sessions
```

### Step 5: Copy Agent Config from Main

```bash
OPENCLAW_DIR=~/.openclaw
cp $OPENCLAW_DIR/agents/main/agent/models.json $OPENCLAW_DIR/agents/{agent_id}/agent/
cp $OPENCLAW_DIR/agents/main/agent/auth-profiles.json $OPENCLAW_DIR/agents/{agent_id}/agent/
```

If the main agent config files don't exist, warn the user and ask them to provide `models.json` and `auth-profiles.json` manually.

### Step 6: Update openclaw.json

**Back up first:**
```bash
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak
```

Read the current config and add the new agent to `agents.list`:

```json
{
  "id": "{agent_id}",
  "name": "{agent_name}",
  "workspace": "~/.openclaw/workspace-{agent_id}",
  "agentDir": "~/.openclaw/agents/{agent_id}/agent"
}
```

Add bindings if provided. For group chat:

```json
{
  "agentId": "{agent_id}",
  "match": {
    "channel": "feishu",
    "peer": {
      "kind": "group",
      "id": "{group_chat_id}"
    }
  }
}
```

For direct chat:

```json
{
  "agentId": "{agent_id}",
  "match": {
    "channel": "feishu",
    "peer": {
      "kind": "direct",
      "id": "{user_id}"
    }
  }
}
```

### Step 7: Install Skills (optional)

If the agent needs specific skills:
```bash
cp -r ~/.openclaw/skills/{skill-name} ~/.openclaw/workspace-{agent_id}/skills/
```

### Step 8: Restart Gateway

```bash
openclaw gateway restart
```

### Step 9: Verify & Report

Tell the user:
- Agent has been created successfully
- How to interact with it (@ in group chat, or DM)
- How to customize it further (edit SOUL.md, add skills, etc.)

## SOUL.md Template

```markdown
# SOUL.md - {Agent Name}

_{One-line purpose}_

## Core Identity

**You are "{Agent Name}"** — {detailed description}

## Principles

- {principle 1}
- {principle 2}
- {principle 3}

## Style

- {style description}

---

_{Mission statement}_
```

## Final Directory Structure

After creation, the layout should be:
```
~/.openclaw/
├── agents/
│   └── {agent_id}/
│       ├── agent/
│       │   ├── auth-profiles.json
│       │   └── models.json
│       └── sessions/
└── workspace-{agent_id}/
    ├── AGENTS.md
    ├── BOOTSTRAP.md (optional)
    ├── HEARTBEAT.md
    ├── IDENTITY.md (optional)
    ├── SOUL.md
    ├── TOOLS.md
    ├── USER.md
    ├── memory/
    └── skills/ (optional)
```

## Important Notes

- Workspace directory name should use the agent_id (English lowercase + hyphens), e.g. `workspace-brainstorm`
- Agent ID must be lowercase alphanumeric with hyphens only
- Group chat binding requires the bot to be manually added to the group (auto-join needs extra permissions)
- Always back up `openclaw.json` before modifying
- Always copy `models.json` and `auth-profiles.json` to the agents directory
- Use the helper script `scripts/agent_creator.py` to automate the config and directory creation
