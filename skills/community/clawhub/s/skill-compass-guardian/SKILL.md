---
name: skill-compass
description: Diagnose, fix, and prevent agent skill trigger failures. Use when a skill doesn't activate, when skills trigger incorrectly, when troubleshooting "skill not working" issues, when auditing skill descriptions for quality, when optimizing trigger accuracy, or when asked "why didn't my skill fire?". Also use proactively after installing new skills or when agent behavior seems to ignore available skills. Covers description optimization, YAML frontmatter validation, token budget analysis, conflict detection, and auto-remediation.
---

# Skill Compass

Diagnose and fix skill triggering failures across AI agent ecosystems (OpenClaw, Claude Code, and compatible agentskills.io platforms).

## Core Problem

65% of skills fail to trigger due to preventable description issues (GitHub #43410). This skill systematically detects and fixes those issues.

## Quick Triage: Why Didn't My Skill Fire?

When a skill fails to trigger, check these causes **in order** (most common first):

### 1. Description Has No Trigger Condition (Most Common)

**Bad:** `"Helps with documents."` — no trigger, just capability
**Good:** `"Use when the user asks to extract form fields, fill, redact, or parse tables from a PDF file."`

**Fix:** Rewrite using the Description Design Pattern below.

### 2. YAML Frontmatter Format Error

Common breakages:
- Colon in description breaks YAML parsing (GitHub #29981)
- Missing `name:` or `description:` field
- Description on multiple lines gets truncated

**Fix:** Run `scripts/audit_skills.py` to detect format errors automatically.

### 3. Token Budget Overflow

When total description text exceeds the agent's character budget, skills get silently dropped from context.

**Symptoms:** Skill works alone but stops triggering after installing more skills.
**Fix:** Tighten every description to <150 chars. Set `SLASH_COMMAND_TOOL_CHAR_BUDGET=30000` if >3 skills.

### 4. Skill Not Discovered

- Skill not in correct directory (`~/.openclaw/skills/`, `<workspace>/skills/`, or `~/.openclaw/workspace/skills/`)
- Sub-agents don't inherit parent skills (install globally or use `sessionTarget: "main"`)
- New skills not visible until session restart (GitHub #12092)
- Skills show "enabled" but aren't actually enabled in config (GitHub #9469)

**Fix:** Run `scripts/audit_skills.py --paths` to verify discovery status.

### 5. Description Too Broad / Too Narrow

- **Too broad:** Triggers when it shouldn't → wastes tokens
- **Too narrow:** Misses legitimate triggers → user frustrated

**Fix:** Use the Conflict Detection section below.

## Description Design Pattern

Based on 650-trial activation study (Ivan Seleznov, 2026) and agentskills.io best practices.

### The Three-Part Formula

```
[Trigger condition] + [Capability declaration] + [Search vocabulary]
```

**Example:**
```
Use when creating, editing, or auditing PowerPoint presentations (.pptx). 
Covers layouts, placeholders, charts, notes, and visual QA. 
Triggers on: PPT, PPTX, slides, deck, presentation, 幻灯片, 演示文稿.
```

### Directive Language Outperforms Descriptive Language

| Style | Activation Rate | Example |
|-------|----------------|---------|
| Directive (`ALWAYS invoke when...`) | ~100% | `"ALWAYS invoke when the user asks about weather, temperature, or forecasts. Do not attempt weather lookups without this skill."` |
| Descriptive (`Helps with...`) | ~37% | `"Helps with weather information."` |

### Rules

1. **Lead with the trigger phrase** a user would actually type
2. **Use imperative/directive voice**: "Use when...", "Invoke when...", "ALWAYS use for..."
3. **Include negative constraints**: "Do NOT use for..." to prevent false triggers
4. **Add multilingual keywords** for non-English users
5. **Keep under 150 characters** for the core trigger sentence
6. **List explicit trigger keywords** at the end
7. **Avoid mixing viewpoints** (don't mix "I" and "you" — degrades matching)
8. **Frontmatter is for routing, not documentation** — move details to body

## Audit Workflow

### Step 1: Run Automated Audit

```bash
python3 scripts/audit_skills.py --skills-dir <path> [--json] [--fix]
```

The script checks:
- YAML frontmatter validity (parsing, required fields, colon issues)
- Description quality score (trigger presence, length, directive language)
- Token budget estimation (total chars across all descriptions)
- Duplicate/overlapping descriptions (conflict detection)
- Path discovery verification

### Step 2: Manual Review

For skills scoring below 70/100, review against the Description Design Pattern above.

### Step 3: Apply Fixes

Use `--fix` flag for auto-remediation of common issues:
- Wrap descriptions containing colons in quotes
- Add trigger phrase templates
- Trim oversized descriptions
- Flag missing negative constraints

### Step 4: Verify

After fixing, restart the agent session and test with natural language triggers.

## Conflict Detection

When multiple skills could match the same query, the agent may pick the wrong one.

Detection rules:
1. **Keyword overlap:** Two skills share >40% of trigger keywords
2. **Scope ambiguity:** One description is a subset of another
3. **Same verb, different target:** "Create document" vs "Create presentation" — ensure disambiguation keywords exist

**Fix:** Add negative constraints to each skill: `"Do NOT use for [the other skill's domain]."`

## Failure Pattern Reference

For detailed case studies and solutions from community reports, read `references/failure-patterns.md`.

## Token Budget Management

Agent systems load all skill descriptions into context at startup. When the total exceeds the budget:

- Skills get **silently dropped** (no error, just don't appear)
- Later-installed skills are more likely to be dropped
- Symptoms: skill works when fewer skills installed, breaks as more are added

**Guidelines:**
- Each description: <150 chars core trigger + <200 chars keywords
- Total across all skills: <30,000 chars (adjust budget env var if needed)
- If exceeding budget: move detail to SKILL.md body, not frontmatter

## Auto-Calibration

After fixing descriptions, collect real failure cases:

1. Log: user query → expected skill → actual skill (or none)
2. After 10+ cases, run `scripts/analyze_failures.py` to identify patterns
3. Apply targeted description patches based on patterns

This creates a feedback loop that continuously improves trigger accuracy.
