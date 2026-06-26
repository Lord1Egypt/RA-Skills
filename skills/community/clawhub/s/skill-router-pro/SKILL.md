---
name: skill-router-pro
description: |
  Skill router and discovery assistant. Use when:
  - User says "I want to do XXX, what skill do I have" or "is there a skill for XXX"
  - User doesn't know which local skill to use for a task
  - User says "what skill should I use" or "find me a skill"
  - User wants to search ClawHub before building a new skill
  - User says "search ClawHub for XXX" or "is there a skill on ClawHub for XXX"
  - User asks "what skills do I have" or "show me my skill list"
  - User says "I don't know which skill to use"
  - Any trigger: "有什么 skill", "帮我找 skill", "what skill", "find me a skill", "skill for"
  Always check here BEFORE building a new skill. If a local or ClawHub skill exists, use it.
---

# Skill Router Pro

Finds existing local skills or searches ClawHub before you build anything new.

## The Problem This Solves

Skills get installed but nobody remembers what's available. This is the first skill to ask
before writing a new one.

## Step 1: Check Local INDEX

Read `~/.openclaw/skills/INDEX.md` and search by keyword.

If a matching skill is found:
- Tell the user the skill name and what it does
- Point them to the install location

## Step 2: Search ClawHub

If nothing local matches, run:

```
clawhub search "<task keywords>"
```

Present results with:
- Skill name and description
- Install command: `clawhub install <name>`

## Step 3: Nothing Found

If neither local nor ClawHub has a match, say:
"No existing skill found for this task. Building a new one is a good option."

Do NOT invent or assume a skill exists.

## Keeping INDEX.md Updated

After installing any new skill, rescan and update the index:

```
find ~/.openclaw/skills ~/mind_claw ~/.codex/skills ~/.cursor/skills-cursor -name "SKILL.md" 2>/dev/null
```

Extract name and description from each SKILL.md frontmatter, then write to
`~/.openclaw/skills/INDEX.md` with this format:

```
# Skill Index

## [Category Name]
| Name | Description | Path |
|------|-------------|------|
| skill-name | What it does | /path/to/skill |
```

## Decision Flow

User asks "I want to do XXX, what skill do I have?"

1. Read INDEX.md
2. Search for "XXX" keyword
3. If found locally: use it
4. If not found: clawhub search "XXX"
5. If on ClawHub: offer install command
6. If nowhere: suggest building one

## Never Do This

- Do not assume a skill exists without checking
- Do not suggest building when ClawHub has one
- Do not leave INDEX.md stale after new installs
- Do not guess — show the index and let the user verify

## Quick Reference

| Situation | Action |
|-----------|--------|
| "what skills do I have" | Show full INDEX.md |
| "I want to do XXX, what skill" | Search INDEX, then ClawHub |
| "search ClawHub for XXX" | Run clawhub search |
| "which skill should I use" | Read INDEX, show matches |
| "build a new skill" | First run skill-router to check if one exists |
