---
name: soulforge
version: "1.0.0"
description: Evolves your SOUL.md automatically based on who you actually are — not who you thought you were when you wrote it. Watches your conversations, decisions, tone, and recurring patterns across sessions. Surfaces insights. Proposes edits. Your agent's soul grows with you. Triggers on: "update my soul", "what have I become", "forge my soul", "reflect on me", "what patterns do you notice", "evolve my soul", or automatically after every 10 sessions.
homepage: https://github.com/Taha2053/soulforge
metadata:
  clawdbot:
    emoji: "🔥"
    requires:
      env: []
    files:
      - "scripts/*"
---

# SoulForge — Your Soul, Evolving

> You wrote your SOUL.md once. But you've changed since then.

Every OpenClaw agent has a SOUL.md — a file that defines who it is. It gets read on every wake. It shapes every response. It's the closest thing to identity an AI agent has.

But there's a problem: **you wrote it once, and it never changed.**

SoulForge watches who you actually are across sessions — your real decisions, your recurring phrases, your values in action, your blindspots — and evolves your SOUL.md to match. Not who you aspired to be. Who you are.

---

## External Endpoints

| Endpoint | Purpose | Data Sent |
|---|---|---|
| None | Fully local analysis | Nothing leaves your machine |

SoulForge reads your local session history and SOUL.md only. All analysis is local. No telemetry. No external API calls.

---

## Security & Privacy

- **Zero external calls.** Everything happens on your local filesystem.
- **No credentials required.** No API keys, tokens, or env vars.
- **Read-mostly.** SoulForge reads session history and only writes to SOUL.md with your explicit approval.
- **You approve every change.** SoulForge never silently edits your soul. It proposes — you decide.
- **Your data stays yours.** Session history never leaves your machine.

> **Trust Statement:** SoulForge reads files you already have locally (SOUL.md, session logs) and proposes edits for your review. Nothing is transmitted anywhere. You have full control over every change.

---

## Model Invocation Note

SoulForge can be invoked manually at any time. It also runs a lightweight passive observation pass automatically every 10 sessions — surfacing patterns without changing anything unless you ask it to. You can disable auto-observation by adding `soulforge: observe: false` to your OpenClaw config.

---

## What SoulForge Does

### 1. 👁️ Observes (passive, automatic)
Every session, SoulForge quietly notes:
- Recurring phrases and vocabulary you actually use
- Topics you return to unprompted
- How you handle disagreement, uncertainty, pressure
- What you ask for vs. what you actually want
- Patterns in your decisions over time
- Emotional register: when you're focused, frustrated, curious, playful

Nothing is stored externally. Observations accumulate locally in `memory/observations.json`.

### 2. 🔍 Reflects (on demand or every 10 sessions)
When triggered, SoulForge surfaces what it's noticed:

```
"Over the last 3 weeks, I've noticed:
- You consistently push back on vague answers — you want precision
- You start most sessions with a task but end them with a question
- You say 'actually' before your real opinion, not your first one
- You've mentioned your project 14 times but never asked for help with it
- Your tone shifts at night — more reflective, less task-driven

Want me to propose updates to your SOUL.md based on this?"
```

### 3. ✏️ Proposes (with your approval)
SoulForge generates a diff — a clear, readable set of proposed changes to your SOUL.md. You see exactly what would change and why. You accept, reject, or edit each one.

```
PROPOSED CHANGE — Communication Style:

CURRENT:  "I prefer direct answers."
PROPOSED: "I prefer direct answers. I push back on vague responses — 
           ask me to commit to a position if I'm hedging."

REASON: You've explicitly asked for specificity 11 times in 3 weeks.

[Accept] [Reject] [Edit]
```

### 4. 🔥 Forges (applies approved changes)
Once you approve, SoulForge writes the changes to your SOUL.md, backs up the previous version to `backups/soul-YYYY-MM-DD.md`, and logs the change with a timestamp and reason.

Your agent wakes up tomorrow and reads a soul that actually fits.

---

## Trigger Phrases

```
"Update my soul"
"What patterns have you noticed in me?"
"Forge my soul"
"Reflect on who I've become"
"What have you observed about me?"
"Does my SOUL.md still fit?"
"Evolve my soul based on what you know"
"What would you change about my soul file?"
"Run soulforge"
"Soul check"
```

Or automatically, every 10 sessions (configurable).

---

## What SoulForge Tracks

| Signal | What It Captures |
|---|---|
| Vocabulary patterns | Words and phrases you actually use vs. never use |
| Topic gravity | Subjects you return to without being prompted |
| Decision style | How you handle tradeoffs, uncertainty, reversals |
| Tone fingerprint | Your register across contexts — work, personal, creative |
| Aspiration gaps | Things declared in SOUL.md that don't show up in behavior |
| Blindspots | What you consistently avoid, deflect, or underestimate |
| Time patterns | How your communication changes by time of day or session length |
| Engagement spikes | What makes you go deep vs. skim |

---

## The Aspiration Gap

The most powerful thing SoulForge does is detect the gap between **who you said you are** in your SOUL.md and **who you actually are** in your sessions.

Examples of aspiration gaps SoulForge catches:

> *"Your SOUL.md says you value brevity, but you've asked for more detail 23 times and never asked for a shorter answer."*

> *"Your SOUL.md says you prefer async communication, but you always respond within 2 minutes."*

> *"Your SOUL.md says you're decisive, but you've changed direction mid-task 8 times this month."*

These gaps aren't failures — they're data. SoulForge surfaces them without judgment and asks what you actually want your soul to say.

---

## Soul History

Every version of your SOUL.md is preserved in `backups/`. You can restore any previous version:

```
"Restore my soul from last week"
"Show me how my soul has changed over time"
"Undo the last soulforge update"
```

SoulForge also generates a **Soul Timeline** — a readable changelog of who you've become, one soul version at a time.

---

## Example: A Soul Evolution Over 30 Days

**Day 1 SOUL.md excerpt:**
```
I am decisive and prefer moving fast over perfecting.
I value brevity in responses.
I work best in the mornings.
```

**Day 30 SOUL.md excerpt (after SoulForge):**
```
I move fast on reversible decisions. I slow down on people and 
architecture — ask me to flag which kind a decision is before 
I commit.

I value brevity until a topic matters to me. If I start asking 
follow-up questions, go deeper — I'm engaged.

I work best in the mornings for execution. I think best at night — 
save complex open questions for evening sessions.
```

The second version is truer. Not better — truer. And a truer soul makes your agent more useful to you every single day.

---

## File Structure

```
soulforge/
├── SKILL.md                     ← You are here
├── README.md                    ← Install guide
├── scripts/
│   ├── observe.py               ← Passive session observer
│   ├── reflect.py               ← Pattern analysis + insight generator
│   └── forge.py                 ← Diff generator + SOUL.md writer
└── memory/
    ├── observations.json        ← Accumulated session signals
    ├── soul-baseline.md         ← Copy of SOUL.md at install time
    └── backups/                 ← All previous SOUL.md versions
```

---

## Philosophy

Your soul file should feel like a mirror, not a resume.

A resume is who you want others to think you are. A mirror shows who you actually are. SoulForge turns your SOUL.md from a resume into a mirror — and updates it every time you change.

The goal isn't a perfect soul file. The goal is an honest one.
