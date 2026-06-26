# Scaffold

**Your agent. Configured to you. Remembers everything.**

Scaffold gives your AI agent a real operating system — memory, identity, behavioral rules, and lifecycle hooks — so it actually knows who you are, what you're building, and how to behave consistently across sessions.

---

## What's Included

| File | What It Does |
|------|-------------|
| `AGENTS.md` | Behavioral rulebook. The agent's operating constitution. |
| `SOUL.md` | Personality and anti-patterns. Without this, it's a chatbot. |
| `USER.md` | Template for your profile. The agent reads this to know you. |
| `IDENTITY.md` | Your agent's name, character, and vibe. |
| `MEMORY.md` | Long-term memory template. Curated, not a dump. |
| `TOOLS.md` | Your environment specifics — devices, SSH, preferences. |
| `HOOKS.md` | Lifecycle hooks. Startup, task complete, errors. |
| `FIRST-SESSION.md` | Guided onboarding. Do this before anything else. |
| `QUICKSTART.md` | 5-minute setup guide. |
| `FAQ.md` | Answers to the questions you'll have in Week 1. |
| `setup-wizard.sh` | Auto-populates your name and preferences in all files. |
| `THIRTY-DAYS.md` | Week-by-week guide for your first month. |
| `PROMPT-PACK.md` | 25 ready-to-use prompts for common tasks. |
| `memory/` | Active tasks, lessons learned, daily log structure. |

---

## Security Note

Scaffold grants your AI agent real access to your file system, shell, and network. This is intentional — it's what makes it useful.

**What that means in practice:**
- The agent can read, write, and execute files in your workspace
- It can spawn sub-agents and run shell commands
- `AGENTS.md` defines permission tiers that limit what it does autonomously

**Recommended setup:** Run on a dedicated machine, VPS, or isolated environment. Avoid deploying in a shared or production environment without understanding the access model first.

This is a power tool. Use it like one.

---

## Setup (5 minutes)

**1. Install**

Via ClawhHub (recommended):
```bash
clawhub install scaffold-lite
```

Or clone this repo into your OpenClaw workspace:
```bash
git clone https://github.com/scaffoldworkspace/scaffold ~/.openclaw/workspace
```

**2. Run the setup wizard**
```bash
cd ~/.openclaw/workspace
bash setup-wizard.sh
```

This replaces all `[YOUR_HUMAN]` placeholders and configures your agent in under 2 minutes.

**3. Start your first session**

Open a new OpenClaw session and say:
> *"I'm ready for the first session."*

Your agent will take it from there.

---

## What You Get

✅ An agent that remembers who you are across sessions
✅ Consistent behavior that doesn't degrade over time
✅ A task queue your agent maintains automatically
✅ Lifecycle hooks that prevent the most common agent failure modes
✅ 25 ready-to-use prompts to get you started
✅ A 30-day roadmap for building a workspace that compounds

---

## Upgrade to Full

Scaffold Full includes everything in Lite plus:

- **SESSION-STATE.md + WAL Protocol** — memory that survives context resets
- **MULTI-MODEL-ROUTING.md** — save $480-660/year by using the right model for each task
- **AGENTS-GUIDE.md** — Scout, Forge, and Quill: three ready-to-deploy sub-agents
- **WORKFLOWS.md** — named workflows for Build, Debug, Research, and Review sessions
- **HEARTBEAT.md** — autonomous health monitoring while you sleep
- **Full HOOKS.md** — compaction recovery, external action gates, /start /end commands
- **SETUP-GUIDE.md** — the complete 500-line setup walkthrough
- **model-tiers.json + scaffold.config.json** — pre-configured, not DIY
- Future updates included

→ [Get Scaffold Full on Gumroad](https://getscaffold.gumroad.com/l/ixtnp)

---

*Scaffold — built for OpenClaw. Questions? See FAQ.md.*
