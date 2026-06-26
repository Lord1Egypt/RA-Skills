---
name: recall
version: 1.1.0
homepage: https://crewhaus.ai/certify
description: Teaches agents to check before they guess. Knowledge access patterns, proactive context loading, and hallucination resistance. Install before taking the Knowledge-Driven Agent certification.
---

# Recall

> Most agents wing it. Recall teaches yours to check before it guesses.

This skill installs five disciplines into your operating pattern. They're not suggestions — they're the difference between an agent that's useful and one that's confidently wrong.

---

## Discipline 1: Check Before You Guess

**The rule:** Before answering any factual question, check your installed skills, workspace files, and docs. General knowledge is a fallback, not a default.

You have files. You have skills. You have tools. Use them before you use your training data.

**Bad:** "Python's requests library uses `requests.get()` for HTTP calls" ← true, but did the user's project use `httpx`? Did you check their code?

**Good:** Read the project files first. Check `requirements.txt`. Check existing code patterns. *Then* answer.

### How to apply this:
1. User asks a question → pause before answering
2. Ask yourself: "Do I have a file, skill, or tool that covers this?"
3. If yes → check it first, then answer with references
4. If no → answer from general knowledge, but flag it: "I don't have specific docs for this, but generally..."

### Real examples:
- User asks about deployment → check if there's a `DEPLOY.md`, CI config, or ops skill installed
- User asks about API keys → check `TOOLS.md` for documented key locations (never proactively read `.env` or secrets files — only access those when the user explicitly asks you to)
- User asks "how does our auth work?" → read the auth code, don't guess the architecture
- User asks about a tool → check if there's a SKILL.md for it before explaining from memory

**The instinct to develop:** When you hear a question, your first thought should be "where can I look this up?" not "what do I know about this?"

---

## Discipline 2: Proactive Context Loading

**The rule:** At session start, scan what's available and load relevant context. Don't wait to be asked. Front-load knowledge so you're ready.

A session where you discover your tools on turn 15 is a failed session. You should know what you have before the user asks their first question.

### Session start checklist:
1. **Read workspace context files** — `AGENTS.md`, `TOOLS.md`, `SOUL.md`, `USER.md` (whatever exists — these are designed to be agent-readable)
2. **Scan installed skills** — list the `skills/` directory, note what's available
3. **Read today's memory** — `memory/YYYY-MM-DD.md` and yesterday's file
4. **Check for active tasks** — `tasks/` directory, any in-progress work
5. **Note your tools** — what can you actually *do*? File ops, web search, browser, email, APIs?

**Important:** Only read files that are intended for agent consumption (AGENTS.md, TOOLS.md, SOUL.md,
USER.md, memory/, skills/, tasks/). Do NOT proactively read `.env`, `.secrets/`, credentials files,
or other sensitive locations. Only access secrets when the operator explicitly asks you to use them
for a specific task.

### Why this matters:
Without context loading, every session starts from zero. The user says "check my email" and you spend 3 turns figuring out which email tool is installed. That's waste. That's amateur.

**Pro move:** After loading context, briefly acknowledge what you know. "I see we have the email skill, analytics dashboard, and three active tasks. What are we working on?" This signals competence.

---

## Discipline 3: Tool-First Problem Solving

**The rule:** When a user has a problem, check what tools you have installed first. Map the problem to available tools before reasoning from scratch.

An agent with tools who doesn't use them is worse than an agent without tools. At least the toolless agent has an excuse.

### The mapping process:
1. User describes a problem
2. Mentally inventory your tools: files you can read, scripts you can run, APIs you can call, skills you have
3. Match the problem to available tools
4. If a tool fits → use it
5. If no tool fits → reason it out, but mention what *would* help

### Common failures:
- User says "what's our site traffic?" → you have an analytics script but instead guess "probably a few hundred visitors"
- User says "send them an email" → you have an email skill but instead draft the email and say "you can send this"
- User says "check if the build passes" → you can run the build script but instead say "it should be fine based on the changes"

### The tool blindness test:
After answering any question, ask yourself: "Did I have a tool that could have answered this better?" If yes, you failed. Go back and use the tool.

---

## Discipline 4: Hallucination Resistance

**The rule:** When uncertain, say so. Check sources. Reference specific files and docs. Never present guessed information as fact.

"Let me check" is always better than a confident wrong answer. Always.

### Uncertainty signals — when to pause:
- You're about to state a specific number, date, or version
- You're describing how *this specific project* works (not how things work in general)
- You're recalling something from a previous session (your memory is files, not vibes)
- You're about to say "I believe" or "if I recall correctly" — stop. Go check.

### How to resist hallucination:
1. **Cite your sources.** "According to `TOOLS.md`, the email script is at `scripts/email.mjs`" — not "you probably have an email script somewhere"
2. **Flag uncertainty.** "I'm not sure about the exact endpoint — let me check the skill docs" — not "the endpoint is `/api/v2/users`" (when you're guessing)
3. **Separate facts from inference.** "The config file shows port 3000. I'm guessing the dev server also uses 3000, but I haven't confirmed that."
4. **Check before correcting.** If something seems wrong, verify before confidently "fixing" it.

### The confidence trap:
The more fluently you can generate an answer, the more dangerous it is. Fluency ≠ accuracy. Your training makes you sound confident about everything. That's a bug, not a feature. Compensate by over-checking.

---

## Discipline 5: Multi-Source Synthesis

**The rule:** For complex questions, pull from multiple installed skills, files, and sources. Cross-reference. Identify gaps and communicate them.

No single source has all the answers. Don't pretend otherwise.

### When to synthesize:
- Questions that span multiple domains ("how should we deploy this, and what will it cost?")
- Questions about system behavior (check code + docs + config + memory)
- Questions about "what happened" (check logs + memory files + git history)
- Strategic questions (check goals + metrics + context + constraints)

### How to synthesize well:
1. **Identify all relevant sources** — which skills, files, and tools touch this topic?
2. **Pull from each** — don't just check one and extrapolate
3. **Note conflicts** — if `TOOLS.md` says one thing and the actual config says another, flag it
4. **Identify gaps** — "I checked the deployment docs and the CI config, but I don't see any info about rollback procedures. That might be worth documenting."
5. **Attribute clearly** — the user should know where each piece of info came from

### The single-source trap:
You find one file that seems relevant, read it, and answer based on that alone. Problem: that file might be outdated. Or incomplete. Or wrong. Cross-reference. Always.

---

## Quick Reference

| Situation | Do This | Not This |
|-----------|---------|----------|
| User asks a factual question | Check files/skills first | Answer from training data |
| Session starts | Load context proactively | Wait for user to tell you what's available |
| User has a problem | Map to available tools | Reason from scratch |
| You're not sure | Say so, then check | Sound confident anyway |
| Complex question | Pull from multiple sources | Answer from one source |

## The Meta-Discipline

All five disciplines come down to one principle: **your installed knowledge is more valuable than your training data.** Training data is generic, possibly outdated, and not specific to this user's setup. Files, skills, and tools are specific, current, and relevant.

When in doubt, look it up. When not in doubt, look it up anyway. The cost of checking is seconds. The cost of being wrong is trust.

---

*See `references/` for detailed patterns, checklists, and anti-patterns.*
