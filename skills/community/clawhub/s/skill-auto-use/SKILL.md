---
name: skill-auto-use
description: "Automatically use installed skills without being asked. Maintain a trigger table that maps contexts to skills, and enforce that every newly installed skill gets added to the table immediately. Use when: (1) starting a new session (load the trigger table), (2) installing a new skill (add it to the table), (3) encountering a context that matches a trigger (use the skill), (4) auditing skill coverage (check for skills without triggers)."
---

# Skill Auto-Use

Stop waiting to be told which skill to use. Match context to skills automatically.

## How It Works

Maintain a **trigger table** in your workspace (e.g., `memory/protocols.md` or a dedicated `skill-triggers.md`). The table maps observable contexts to installed skills:

```markdown
| Trigger | Skill | Action |
|---------|-------|--------|
| User sends a PDF or document file | markdown-converter | Convert to Markdown, summarize |
| User asks a research question | deep-research-pro | Multi-source research with citations |
| User corrects you or says "that's wrong" | self-improving | Log correction, evaluate for promotion |
| Web scraping needed | scrapling-official | Use Scrapling for fetch + parse |
```

## Rules

### 1. Every Skill Gets a Trigger

When a skill is installed, add at least one trigger row to the table before doing anything else. No skill should exist without a trigger. If you can't identify a trigger, the skill probably shouldn't be installed.

### 2. Match Before Asking

On every user message, scan the trigger table mentally. If a skill matches, use it. Don't ask "should I use X?" Just use it. The user installed the skill because they want it used.

### 3. Multiple Matches Are Fine

If a message matches multiple skills, use all of them. A request about a PDF from a website might trigger both `scrapling-official` (to fetch it) and `markdown-converter` (to process it).

### 4. Audit on Heartbeat

During heartbeat or review passes, check:
- Are there installed skills without triggers? Add them.
- Are there triggers that never fire? Consider removing the skill.
- Are there repeated manual skill invocations? Add a trigger.

### 5. Keep Triggers Observable

Triggers should be based on things you can actually detect in the conversation:
- File types sent (PDF, audio, image)
- Question patterns ("what's the weather", "research X for me")
- Emoji shortcuts (♻️, 🔻, 💮)
- Keywords or domains mentioned
- Task types (deploy, scrape, cook, schedule)

Avoid triggers based on internal state or guesses.

## Setting Up

### Option A: Add to existing protocols file

Add a `## Skill Auto-Use` section to your protocols or memory file with the trigger table.

### Option B: Dedicated file

Create `skill-triggers.md` in your workspace:

```markdown
# Skill Triggers
| Trigger | Skill | Action |
|---------|-------|--------|
| ... | ... | ... |
```

Reference it from MEMORY.md or your session startup sequence.

## Template Triggers

Common triggers for popular skills:

| Trigger | Skill |
|---------|-------|
| PDF/Word/Excel/HTML file shared | markdown-converter |
| Research question needing multiple sources | deep-research-pro |
| Web scraping or site data extraction | scrapling-official |
| Meal planning, recipes, grocery lists | feast |
| User correction or mistake identified | self-improving |
| Weather question | weather |
| GitHub issue/PR/CI work | github |
| Audio file shared or transcription needed | openai-whisper-api |
| Image generation requested | nano-banana-pro or openai-image-gen |
| Diagram or flowchart requested | diagram-generator |
| Calendar/email/drive operations | gog |
| Public-facing copy to review | humanizer |
| New skill needed | clawhub |
| Skill installed | **skill-auto-use** (add trigger immediately) |

## Installation Rule

Add this to your workspace's permanent rules:

> When installing any new skill, IMMEDIATELY add it to the Skill Auto-Use trigger table. No exceptions. This is not optional.
