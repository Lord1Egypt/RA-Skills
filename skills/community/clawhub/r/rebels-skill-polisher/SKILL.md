---
name: skill-polisher
description: >
  Polishes standalone skills and multi-skill bundles for ClawHub readability without
  sacrificing LLM effectiveness. Use when improving a skill's listing, making a skill look
  better on ClawHub, or preparing a skill for publish. Supports cross-skill dependency
  mapping and regression checking for bundles. Moved content goes to references/ — never
  deleted.
---

# Skill Polisher 🪚

**Improve a skill's SKILL.md for ClawHub readability.** Run after the skill is built and tested — never before.

Works in two modes: **standalone** (single skill) and **bundle** (multi-skill with shared infrastructure and cross-skill data contracts). Mode is auto-detected.

## Why

A well-formatted SKILL.md gets more installs on ClawHub. But polish shouldn't come at the cost of LLM effectiveness — the agent still needs every instruction to do its job correctly. This skill rewrites for readability, then audits to ensure nothing important was lost.

## When to Use

- "Make this skill look better on ClawHub"
- "Polish my SKILL.md"
- "Improve this skill's listing"
- "Polish my bundle"
- "Clean up these skills"

## ⚠️ When NOT to Use

- On extracted sub-skills from a bundle install (advise user to point at the full bundle source)
- On skills that aren't functionally working yet
- As a replacement for the skill-creator — polish after building, not during

## How It Works

**Standalone:**
```
1. Read the existing SKILL.md
2. Rewrite for readability (apply rules from references/)
3. Audit the rewrite against the original
4. Output: polished SKILL.md + audit report + reference files
```

**Bundle:**
```
1. Detect bundle structure
2. Build dependency map (field names, paths, references)
3. Clean stale §X.Y architecture references
4. For each sub-skill: rewrite → update cross-refs → regression check → audit
5. Cross-validation pass (final contract verification)
6. Output: polished files + audit reports + reference files
```

See [references/bundle-rules.md](references/bundle-rules.md) for the full bundle workflow.

## Before Polishing

```
✅ Functionally working (scripts tested)
✅ Description triggers on the right queries
```

If either fails, fix first. Don't polish a broken skill.

## 🪚 Polishing Rules

Read [references/rules.md](references/rules.md) for the full set. Key principles:

```
Short paragraphs (1-2 lines)     — dense blocks kill readability
Code blocks for lists            — renders as visual boxes on ClawHub
Emoji as section anchors         — 🔒 📊 ⚡ give instant visual context
One code block per concept       — not three variations for three platforms
Protected content stays inline   — behavioral contracts never get moved
```

## 📦 What Gets Moved to references/

```
Platform-specific formatting  → references/formatting.md
Detailed auth/token setup     → references/setup.md
Extended configuration        → references/configuration.md
API details / error handling  → references/api.md
Historical changelogs         → references/changelog.md
```

**Rule: Content is moved, never deleted.**

**Exceptions — never move:**
- Anti-hallucination / data integrity rules
- Safety constraints ("does NOT do", "what NOT to do")
- Confirmation requirements
- Display format contracts
- Cross-skill data contracts (bundle mode)
- Post-flow output (end-of-turn sections, offers)

See [references/rules.md](references/rules.md) for the full protected content table.

## 🔒 The Audit

After rewriting, compare original against polished. Flag:

```
⚠ Potentially risky changes:
• Protected content moved to references/
• Cross-skill data contract broken
• Security notes removed
• Trigger phrases removed from description
• Reference files created but empty or incomplete
```

See [references/audit-guide.md](references/audit-guide.md) for the full checklist.

## 📊 Output

**Standalone:** polished SKILL.md + reference files + audit report.

**Bundle:** polished SKILL.md per sub-skill + reference files + audit per sub-skill + cross-validation report.

Wait for user approval before overwriting originals.
