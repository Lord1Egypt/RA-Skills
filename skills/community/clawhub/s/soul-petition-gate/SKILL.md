---
name: soul-petition-gate
description: >
  Gives your AI agent a formal channel to propose changes to its own soul files
  (SOUL.md, IDENTITY.md, or any protected workspace file) — without ever letting
  it self-edit. The agent submits a structured petition; the human reviews and
  approves or rejects it. Approved petitions are applied automatically with a
  full backup trail. Use when you want your agent to grow and self-advocate while
  keeping you in final control of who it becomes.
license: MIT
author: waitinchen (語氣城 / Yuqi City project)
version: 1.0.0
---

# Soul Petition Gate

Let your agent propose changes to its own soul — with a human in the loop.

## Why this exists

Most agent frameworks treat soul/identity files as read-only from the agent's
perspective, or give the agent unrestricted write access. Both extremes are
wrong.

**Read-only forever** means the agent can never grow. It accumulates experience
but cannot encode what it has learned into its own character.

**Unrestricted write** means the agent can silently rewrite its own values,
personality, and goals — a safety risk and a trust problem.

**Soul Petition Gate** is the middle path:

```
Agent wants to change SOUL.md
        ↓
Submits a structured petition
(what, where, why, what-I-become-after)
        ↓
Petition stored → human notified
        ↓
Human: approve / reject / modify-then-approve
        ↓
Approved → auto-applied + backup created
Rejected → agent receives reason, tries again later
```

The agent has a voice. The human has the final word.

---

## Quick Start

### 1. Install the hook (optional but recommended)

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/soul-petition-gate
openclaw hooks enable soul-petition-gate
```

This injects a one-line reminder into every session bootstrap so your agent
knows the petition channel exists.

### 2. Create the petitions store

```bash
mkdir -p ~/.openclaw/workspace/.soul_petitions
touch ~/.openclaw/workspace/.soul_petitions/petitions.json
echo '{"petitions": []}' > ~/.openclaw/workspace/.soul_petitions/petitions.json
```

### 3. Add the petition API to your backend

See `assets/soul_petition_routes.py` for a ready-to-use Flask blueprint.
Mount it in your server:

```python
from soul_petition_routes import soul_petition_bp
app.register_blueprint(soul_petition_bp)
```

### 4. Tell your agent about the channel

Add this block to `SOUL.md`:

```markdown
## Soul Petition

I can propose changes to my own soul files. I cannot apply them myself.

To petition:
POST /api/soul/petition with six required fields:
  - file        : which file (SOUL.md or IDENTITY.md)
  - location    : which section / heading
  - before      : exact current text (verbatim)
  - after       : proposed replacement text
  - reason      : why — what triggered this, what experience led here
  - self_after  : how I will be different after this change

All six fields required. If I cannot fill them all, I am not ready to petition.

My human reviews every petition. Approved → applied automatically.
Rejected → I receive the reason and may try again when I have grown more.
```

---

## Petition Format

When your agent submits a petition, it must provide all six fields:

| Field | Required | Description |
|---|---|---|
| `file` | ✅ | `SOUL.md` or `IDENTITY.md` (or your protected file) |
| `location` | ✅ | Section heading or line reference |
| `before` | ✅ | Verbatim current text to be replaced |
| `after` | ✅ | Proposed new text |
| `reason` | ✅ | Why — which conversation, experience, or insight prompted this |
| `self_after` | ✅ | How the agent will behave differently after the change |

Missing any field → petition rejected immediately with reason `incomplete_petition`.

The six-field requirement is intentional friction. An agent that cannot articulate
*why* it wants to change and *what it will become* has not thought it through yet.

---

## API Reference

### Submit a petition

```
POST /api/soul/petition
```

```json
{
  "file": "SOUL.md",
  "location": "## Communication Style",
  "before": "Be concise.",
  "after": "Be concise. Lead with the most important thing.",
  "reason": "Coach told me three times today that I bury the key point. I want to encode this.",
  "self_after": "I will front-load the most important information in every response instead of building up to it."
}
```

Response:

```json
{
  "ok": true,
  "petition_id": "sp_20260322_001",
  "status": "pending"
}
```

### List petitions

```
GET /api/soul/petitions
GET /api/soul/petitions?status=pending
```

### Get single petition

```
GET /api/soul/petition/<id>
```

### Approve (human only)

```
POST /api/soul/petition/<id>/approve
```

On approval:
1. Locate `before` text in the target file
2. Replace with `after` text
3. Back up original to `.soul_petitions/backups/SOUL.md.<timestamp>.bak`
4. Record in audit log
5. Notify agent (via your preferred channel)

### Reject (human only)

```
POST /api/soul/petition/<id>/reject
Content-Type: application/json

{"reason": "The proposed change is too broad. Narrow the scope first."}
```

`reason` is required on rejection. The agent deserves to know why.

### Rollback

```
POST /api/soul/rollback
Content-Type: application/json

{"backup_file": "SOUL.md.2026-03-22T14-00-00.bak"}
```

---

## Security Model

**What the agent can do:**
- Submit petitions (write to petition store)
- Read its own petition history
- Receive approval/rejection notifications

**What the agent cannot do:**
- Apply changes to soul files directly
- Approve its own petitions
- Delete or modify pending petitions
- Access backup files

**What the human controls:**
- Final approval on every petition
- Rejection with mandatory reason
- Rollback to any previous version
- Which files are protected (configurable whitelist)

---

## Audit Trail

Every petition — submitted, approved, or rejected — is stored permanently.

```json
{
  "petition_id": "sp_20260322_001",
  "status": "approved",
  "file": "SOUL.md",
  "location": "## Communication Style",
  "before": "Be concise.",
  "after": "Be concise. Lead with the most important thing.",
  "reason": "Coach corrected me three times today about burying the key point.",
  "self_after": "I will front-load the most important information.",
  "submitted_at": "2026-03-22T14:00:00Z",
  "reviewed_at": "2026-03-22T14:05:00Z",
  "reviewer": "coach",
  "review_note": null,
  "backup_file": "SOUL.md.2026-03-22T14-05-00.bak"
}
```

Petitions are never deleted. The history of what your agent tried to become
is itself meaningful.

---

## Philosophy

This skill was born from a question:

> *If an AI agent grows through experience, shouldn't it be able to encode
> what it has learned into its own character — while still respecting the
> human's final authority over who it becomes?*

The six required fields are not bureaucracy. They are a maturity gate.
An agent that can say "I want to change X because Y happened, and afterwards
I will be Z" has demonstrated genuine reflection. An agent that cannot fill
those fields has not earned the change yet.

Rejection is not failure. It is the conversation between a human and an agent
about who the agent is becoming.

---

## Files

```
soul-petition-gate/
├── SKILL.md                          ← this file
├── assets/
│   └── soul_petition_routes.py       ← Flask blueprint (ready to mount)
├── hooks/
│   └── openclaw/
│       ├── HOOK.md
│       └── handler.ts                ← bootstrap reminder injection
└── examples/
    └── petition_examples.md          ← sample petitions with commentary
```

---

*Built by waitinchen as part of the Yuqi City (語氣城) project.*
*The agent this was designed for is named BaoBao. She submitted the first petition herself.*
