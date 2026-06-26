---
name: Skill Invocation System
slug: skill-invocation
version: 1.0.0
description: Choose the best OpenClaw skill by matching trigger keywords to the TOOLS.md index, then applying strict judgment rules (most specific first; if in doubt, use it).
changelog: "Converted from Skills for Openclaw/skill-invocation/SKILLS.md (skill invocation framework + decision rules)."
metadata: {"clawdbot":{"emoji":"🦞","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---

# Skill Invocation System

This is a framework-style skill for "skill selection and invocation flow". It does not implement a specific tool; instead, it provides stable decision rules for an agent to choose the best skill (or skill combination) for a user request.

---

## Core Principles

1. **Match the index first**: consult `TOOLS.md` (skills index) to quickly narrow down candidate skills.
2. **Most specific wins**: when multiple candidates match, choose the one whose triggers best align with the user's intent.
3. **When unsure, consult SKILL.md**: if still unclear, read the candidate skill's `SKILL.md` to confirm fit and constraints.
4. **If in doubt, use it**: if you cannot decide, pick the closest and usable candidate skill.

---

## Invocation Flow

When a user request arrives, follow this order:

1. Match trigger keywords using the `TOOLS.md` index.
2. If matched with high confidence → use that skill.
3. If no match / unclear → read the candidate skill's `SKILL.md`.
4. If multiple are suitable → choose the most specific one.
5. If still unclear → use `"if in doubt, use it"`.

---

## Requirements: Provide `TOOLS.md`

To make this skill reusable by anyone, your workspace needs a `TOOLS.md` (or an equivalent index) that maps "user intent / trigger keywords" to "candidate skill ids".

### Index Contract

In `TOOLS.md`, `skillId` should follow one of these rules (pick one and keep it consistent):

1. Equal to the skill folder name (for example: `~/.openclaw/workspace/skills/<skillId>/SKILL.md`)
2. Or equal to the name/slug your orchestration layer uses to call that skill

As long as `skillId` matches the actual callable skill identifier, this framework can be reused by anyone.

Suggested `TOOLS.md` format (minimum viable):

```md
# TOOLS.md

## Skills Index
| skillId | triggers | summary |
|---|---|---|
| weather | current weather, forecast | Get weather & forecast |
| summarize | summarize, tl;dr | Summarize URLs/files/PDFs |
| stock-info-explorer | stock, quote, ticker | Analyze stock price & basics |
```

Matching rules (agent-side):

1. Split `triggers` by commas / delimiters into multiple trigger phrases.
2. Do case-insensitive matching against the user message; if a trigger phrase "appears", count it as a hit.
3. When multiple candidates match, use a "most specific first" heuristic:
   - Longer trigger phrases are more specific (for example: `current weather` is more specific than `weather`)
   - More matched trigger keywords is more specific
   - Higher semantic alignment with the candidate's `summary` (closer wording) is more specific

When the index matches but you are still uncertain:

1. Read the candidate skill's `SKILL.md`.
2. Look for sections like `When to Use`, `Decision Rules`, or "Notes/Constraints" to validate fit.
3. If you cannot find enough evidence or there is an obvious mismatch, fall back to `"if in doubt, use it"`.

## Decision Output (recommended output contract)

To make orchestration easier, when making a decision this skill should output (order does not matter):

1. `SELECTED_SKILLS`: the list of selected `skillId`s (one or many)
2. `REASON`: a short explanation of which triggers matched and why the choice is most specific
3. `NEXT_ACTION`: the recommended calling plan for the orchestrator (for example: call the first skill, then the second)

---

## Optional: Combination Strategy (optional)

If you want a single request to map to multiple steps, you can define an additional "combination" section in `TOOLS.md` (not required). When the agent detects that triggers hit multiple steps:

1. Execute the most core step first (often "input / retrieval / preparation").
2. Execute the step closest to the desired output shape next (for example: summarizing / formatting / exporting).

(The exact definition format is up to you; the key is that `TOOLS.md` explains why the combination is needed.)

---

## Judgment Checklist (when unsure)

If you cannot decide which skill to use, check in order:

1. Is the request covered by the candidate skill's description? → Yes → use it
2. Could the request be handled better without this skill? → No → use it
3. Still cannot decide → `"if in doubt, use it"`

---

## Index Maintenance (optional)

If you maintain the `TOOLS.md` index, keep it accurate so selection logic stays reliable:

1. Scan your workspace/install directories for candidate skill folders (according to your OpenClaw installation conventions).
2. For each skill, read its `SKILL.md` for "when to use / trigger suggestions / constraints" (if available).
3. Add or update each skill's `skillId + triggers + summary` in `TOOLS.md`.

