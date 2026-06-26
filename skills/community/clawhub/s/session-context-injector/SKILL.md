---
name: session-context-injector
version: 1.0.0
description: "Reorient a Telegram chat after a session reset. Reads a project's STATUS.md (resume point, blockers, next action) and sends a project-specific context injection message via the Telegram bot API. Use when: clearing session transcripts, creating new project rooms, or onboarding collaborators into a scoped chat. Supports 3 message variants: group refresh, direct DM summary, and new-room welcome."
metadata:
  openclaw:
    emoji: "🔄"
    requires:
      bins: ["python3"]
      env: ["TELEGRAM_BOT_TOKEN"]
    network:
      outbound: true
      reason: "Sends messages to the Telegram Bot API (api.telegram.org) to inject context into group chats and DMs after session resets."
    primaryEnv: "TELEGRAM_BOT_TOKEN"
    tags:
      - telegram
      - context-injection
      - session-refresh
      - project-rooms
      - reorientation
      - clawhub
---

# SKILL: session-context-injector

**Use when:** A Telegram chat session has been cleared, a collaborator joins a project room, a new project room is created, or any context needs to be re-anchored in a specific chat after a reset.

**Why this exists:** After a session clear, the next person to message gets a blank-slate AI with no project awareness. This skill ensures every reset is followed by a project-specific reorientation message — so the first reply in a fresh session is always oriented, not confused.

**Invoked by:**
- `playbooks/session-refresh/PLAYBOOK.md` — Phase 3, after each session clear
- `playbooks/new-project/PLAYBOOK.md` — Stage 5b, after room creation
- `playbooks/telegram-collaborator-room/PLAYBOOK.md` — on collaborator join

---

## Inputs

| Input | Source | Required |
|---|---|---|
| `chat_id` | sessions.json or telegram-groups.json | ✅ |
| `slug` | `memory/telegram-groups.json[chat_id].slug` | ✅ for project rooms |
| `project_name` | `memory/telegram-groups.json[chat_id].name` | ✅ |
| `bot_token` | `op read "op://OpenClaw/Telegram Bot Token/credential"` | ✅ |
| `STATUS.md` | `projects/<slug>/STATUS.md` | Optional — enriches message |
| `chat_type` | `group` / `direct` / `tui` | ✅ |

---

## Step 1 — Parse STATUS.md

If `projects/<slug>/STATUS.md` exists, extract:

```python
import re

def parse_status(slug: str) -> dict:
    path = PROJECTS_DIR / slug / "STATUS.md"
    if not path.exists():
        return {}
    text = path.read_text()

    def extract(heading: str) -> str:
        m = re.search(
            rf"##+ {re.escape(heading)}\s*\n(.*?)(?=\n##|\Z)",
            text, re.DOTALL
        )
        return m.group(1).strip()[:400] if m else ""

    resume   = extract("RESUME FROM HERE") or extract("Resume From Here") or ""
    blockers = extract("Blockers") or extract("Open Blockers") or ""

    # Strip markdown bullets
    resume   = re.sub(r"^[-*] ", "", resume, flags=re.MULTILINE).strip()
    blockers = re.sub(r"^[-*] ", "", blockers, flags=re.MULTILINE).strip()

    return {
        "resume":   resume[:300],
        "blockers": blockers[:200],
    }
```

**Fallback:** If STATUS.md is missing or empty, use the generic template (Step 2b).

---

## Step 2a — Build Project Room Message (group chat)

```python
def build_group_message(project_name: str, slug: str, status: dict) -> str:
    resume   = status.get("resume", "")
    blockers = status.get("blockers", "")

    lines = [
        f"🔄 <b>Session Refresh — {project_name}</b>",
        "",
        "I've refreshed my context. Here's where we are:",
        "",
    ]

    if slug:
        lines.append(f"📌 <b>Project:</b> {slug.upper()}")
    if resume:
        lines.append(f"📍 <b>Resume from:</b> {resume}")
    if blockers and blockers.lower() not in ("none", "—", "-", ""):
        lines.append(f"🚧 <b>Blockers:</b> {blockers}")

    lines += [
        "",
        "My memory and project files are fully updated. "
        "Jump back in whenever you're ready — just pick up the thread. 🐾",
    ]
    return "\n".join(lines)
```

**Character limit:** Keep under 4096 chars (Telegram max). Truncate `resume` and `blockers` at the values above if STATUS.md is long.

---

## Step 2b — Build Direct Chat Message (Nissan DM)

Use when `chat_type == "direct"` and the chat_id is Nissan's (`821071206`).

```python
def build_direct_message(touched_projects: list[dict]) -> str:
    lines = [
        "🔄 <b>Daily Session Refresh</b>",
        "",
        "Context cleared. Memory and STATUS files are up to date.",
    ]
    if touched_projects:
        lines.append("")
        lines.append("Active projects refreshed:")
        for p in touched_projects[:10]:
            lines.append(f"• <b>{p['slug'].upper()}</b> — {p['name']}")
    lines += ["", "Anything you want to jump straight into? 🐾"]
    return "\n".join(lines)
```

---

## Step 2c — Build New Room / Collaborator Join Message

Use when a room is freshly created or a collaborator joins for the first time (not a reset).

```python
def build_welcome_message(project_name: str, slug: str, purpose: str, allowed_topics: list[str]) -> str:
    topic_list = "\n".join(f"• {t}" for t in allowed_topics[:8])
    return (
        f"👋 <b>Welcome to {project_name}</b>\n\n"
        f"{purpose}\n\n"
        f"<b>What I can help with here:</b>\n{topic_list}\n\n"
        f"I have full project context loaded. Ask me anything within scope. 🐾"
    )
```

---

## Step 3 — Send via Telegram Bot API

```python
import urllib.request, json

def send_injection(bot_token: str, chat_id: str, text: str, dry_run: bool = False) -> bool:
    if dry_run:
        print(f"[DRY-RUN] → {chat_id}: {text[:100].replace(chr(10),' ')}…")
        return True
    try:
        url     = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = json.dumps({
            "chat_id":    chat_id,
            "text":       text,
            "parse_mode": "HTML",
        }).encode()
        req = urllib.request.Request(
            url, data=payload,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status == 200
    except Exception as e:
        print(f"⚠️  Injection failed ({chat_id}): {e}")
        return False
```

**Parse mode:** Always use `HTML` (not `Markdown`). Markdown requires escaping; HTML is more predictable with `<b>` and `<i>`.

**On failure:** Log the failure, continue with other chats. Never block the refresh loop on a single failed send.

---

## Step 4 — Log the Injection

After each successful send, append to `memory/YYYY-MM-DD.md`:

```markdown
### Context Injection Sent — [project_name] — YYYY-MM-DD HH:MM AEST
- **Chat ID:** [chat_id]
- **Slug:** [slug]
- **Type:** [session-refresh / room-creation / collaborator-join]
- **Status:** ✅ sent / ❌ failed
```

And if the project has a STATUS.md, append a one-liner:

```
_Context injection sent: YYYY-MM-DD HH:MM AEST — session cleared._
```

---

## Decision Rules

| Condition | Action |
|---|---|
| STATUS.md exists + has content | Use Step 2a with extracted resume/blockers |
| STATUS.md missing or empty | Use Step 2a with slug + name only (no resume/blockers section) |
| `chat_type == "direct"` + Nissan | Use Step 2b |
| New room / first join | Use Step 2c |
| `chat_id` is None | Skip Telegram send; log to memory only |
| `bot_token` unavailable | Log failure to memory; do not crash |
| Message > 4096 chars | Truncate `resume` to 200 chars, `blockers` to 100 chars |

---

## Example Output (group chat, STATUS.md found)

```
🔄 Session Refresh — OpenClaw — Portkey Gateway Integration

I've refreshed my context. Here's where we are:

📌 Project: PORTKEY
📍 Resume from: Test latency comparison between direct Anthropic calls and Portkey-routed calls. Script is at scripts/portkey-bench.py — needs --compare flag wired up.
🚧 Blockers: Portkey dashboard shows incorrect token counts for cache_read events — filed upstream.

My memory and project files are fully updated. Jump back in whenever you're ready — just pick up the thread. 🐾
```

---

## Reuse Checklist

Before calling this skill from a playbook or script:

- [ ] `chat_id` is confirmed (from sessions.json or telegram-groups.json)
- [ ] `bot_token` retrieved from 1Password (not hardcoded)
- [ ] `slug` verified — `projects/<slug>/STATUS.md` exists or graceful fallback confirmed
- [ ] `parse_mode: "HTML"` — not Markdown
- [ ] Failure is logged, not raised

---

## ClawHub Tags

`telegram`, `context-injection`, `session-refresh`, `project-rooms`, `reorientation`

---

## Changelog

- **2026-04-03:** Extracted from `playbooks/session-refresh/PLAYBOOK.md` Phase 3. Added welcome/join variant (Step 2c). Formalised as standalone reusable skill.
