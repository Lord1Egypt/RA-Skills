<!--
QUICKSTART.md - Scaffold Fast Setup

WHAT THIS IS: The 5-minute path to a working agent. Skip the manual, get running.
Read the full SETUP-GUIDE.md later - this gets you unblocked fast.
-->

# QUICKSTART.md - Up and Running in 5 Minutes

*Don't want to read the whole guide right now? That's fine. Do this first.*

---

## 3 Steps to Your First Working Session

**Step 1: Drop the files**
Copy everything in this package to your OpenClaw workspace:
```bash
cp -r scaffold-v1.0/* ~/.openclaw/workspace/
```

**Step 2: Open OpenClaw**
Start a new session - web UI, Telegram, or CLI, wherever you use it.

**Step 3: Say this**
> *"Read FIRST-SESSION.md and let's get started."*

That's it. Your agent will guide you through the rest interactively.

---

## What to Customize First (In Order)

1. **SOUL.md** - Your agent's personality. The "Calibrating to Your Human" section fills in automatically over time - don't touch it. But read the rest so you understand what you've got.

2. **USER.md** - Your name, timezone, goals, tools. Your agent reads this every session. Fill it in during FIRST-SESSION.md.

3. **IDENTITY.md** - Your agent's name and vibe. Pick something that fits. Your agent will use this name forever - choose deliberately.

4. **HEARTBEAT.md** - Add at least one infrastructure check specific to your setup. The placeholders are there - fill them in.

---

## First 3 Things to Try

1. *"What files did you just read and what do you know about me so far?"* - calibration check
2. *"What should we set up first?"* - lets your agent take the lead
3. *"Run openclaw models list and tell me what I've got"* - kick off model routing

---

## Where to Go If Something Breaks

| Problem | Go to |
|---------|-------|
| Setup steps not working | SETUP-GUIDE.md Section 2 (Prerequisites) |
| Agent asking same questions each session | SETUP-GUIDE.md Section 5 (Memory System) |
| Heartbeat costing too much | MULTI-MODEL-ROUTING.md TL;DR |
| Sub-agents not running | SETUP-GUIDE.md Section 8 (Sub-Agents) |
| Common questions | FAQ.md |

---

## ⚠️ One Gotcha - Don't Skip FIRST-SESSION.md

It's tempting to jump straight to using your agent. Don't. FIRST-SESSION.md is how your agent learns who you are, what you're building, and what "done" looks like for you. Skip it and you'll spend the next 10 sessions re-explaining yourself.

Takes 15 minutes. Worth every second.

---

*When you're ready to go deeper: SETUP-GUIDE.md covers everything in full detail.*
*Questions: getscaffold@outlook.com*
