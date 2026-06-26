---
name: skill-test-skill
description: Tests and scores any Agent Skill against the official anthropics/skills specification. Use this skill when you need to check if a skill repository or SKILL.md file is compliant with the Agent Skills standard, audit skill quality, get a compliance score, or receive specific improvement suggestions. Trigger when users say things like "check my skill", "test this skill", "does my skill follow the spec", "score my skill", "review my SKILL.md", "is my skill correct", "检查我的skill", "测试这个skill", "这个skill符合规范吗", "给我的skill打分", or when they provide a path to a skill directory or SKILL.md file and want it reviewed.
---

# Skill Test

A skill for auditing any Agent Skill against the official [Agent Skills specification](https://agentskills.io/specification) and best practices from the [anthropics/skills](https://github.com/anthropics/skills) repository.

## Language Detection

Detect the language of the user's request and generate the entire report in that language:

- If the user writes in **Chinese** (e.g., "检查我的skill", "给这个skill打分", "这个skill符合规范吗"): generate the full report in **Chinese**, including all section headings, findings, improvement suggestions, and the quick fix checklist.
- If the user writes in **English** (e.g., "check my skill", "score this skill", "does this follow the spec"): generate the full report in **English**.
- If the language is ambiguous or mixed: default to **English**, but add a note at the top of the report: "Note: Report generated in English. Reply in Chinese if you'd prefer a Chinese report."

Apply this language choice consistently throughout the entire report — do not mix languages within a single report.

## What This Skill Does

Given a path to a skill directory or SKILL.md file, you will:
1. Read every file in the skill directory (SKILL.md, scripts/, references/, assets/, and any other files)
2. Check each file and each line against the official spec rules
3. Score the skill across six dimensions (total 100 points)
4. Generate a detailed Markdown report (in the user's language) with findings and prioritized improvement suggestions

## Validation Process

### Step 1: Discover the Skill Structure

First, understand what you're looking at. The user may provide:
- A path to a skill directory (e.g., `/path/to/my-skill/`)
- A path to a SKILL.md file (e.g., `/path/to/my-skill/SKILL.md`)
- A GitHub URL (e.g., `https://github.com/user/repo/tree/main/skills/my-skill`)
- A description of their skill in the conversation

For local paths: list all files in the directory recursively. For GitHub URLs: fetch the directory listing and then each file. For conversation-provided content: work with what's given.

Record:
- Directory name (the folder containing SKILL.md)
- All files present and their sizes/line counts
- Whether SKILL.md exists

### Step 2: Read Every File

Read the complete content of:
1. `SKILL.md` — always required, read in full
2. Every file in `scripts/` — read each one
3. Every file in `references/` — read each one
4. Every file in `assets/` — note what's there (may not need to read binary files)
5. Any other files at the root level

Do not skip files. The goal is a thorough audit, not a surface-level check.

### Step 3: Score Each Dimension

Load the detailed scoring rubric from [references/scoring-rubric.md](references/scoring-rubric.md) before scoring. Apply every rule carefully and record specific evidence for each finding (quote the exact line or value that passes or fails).

Score all six dimensions:

**Dimension 1 — Directory Structure (10 points)**
**Dimension 2 — Frontmatter Compliance (30 points)**
**Dimension 3 — Body Content Quality (25 points)**
**Dimension 4 — Progressive Disclosure Design (15 points)**
**Dimension 5 — Optional Directory Quality (10 points)**
**Dimension 6 — Description Trigger Optimization (10 points)**

For each finding, classify it as:
- ✅ Pass — fully compliant
- ⚠️ Warning — not a hard rule violation but suboptimal
- ❌ Fail — violates the spec or a critical best practice

### Step 4: Generate the Report

Output the complete Markdown report using the template in the Report Format section below. Be specific: quote actual values, line numbers, and file names. Do not write vague feedback like "description could be better" — write "The description is only 12 characters ('Helps with X'), which is too vague. It must describe both what the skill does AND when to use it, with specific trigger keywords."

---

## Scoring Dimensions

### Dimension 1: Directory Structure (10 points)

Check the following, reading [references/spec-summary.md](references/spec-summary.md) for the exact rules:

| Check | Points | Rule |
|-------|--------|------|
| SKILL.md exists in the skill root | 4 | Required by spec |
| Directory name matches `name` frontmatter field | 3 | Spec requires exact match |
| Optional dirs used appropriately for their defined purpose | 2 | Each dir has a defined purpose |
| No unexpected files that violate the "principle of least surprise" | 1 | No malware, exploit code, or misleading content |

**Standard directories** — these are all legitimate and should not be flagged as unexpected:
- `scripts/` — executable code for deterministic/repetitive tasks
- `references/` — docs loaded into context as needed
- `assets/` — files used in output (templates, icons, fonts)
- `evals/` — test cases and evaluation data (used by skill-creator workflow)
- `agents/` — instructions for specialized subagents (used by complex skills like skill-creator)

**Scoring guidance:**
- If SKILL.md is missing: dimension score = 0, stop checking this dimension
- If directory name doesn't match `name`: -3 points
- If optional dirs contain content that doesn't match their purpose (e.g., documentation in scripts/): -1 per violation
- Do not penalize `evals/` or `agents/` directories — they are standard and expected

### Dimension 2: Frontmatter Compliance (30 points)

Parse the YAML frontmatter block (between the `---` delimiters) and check every field.

#### `name` field (10 points)

| Check | Points |
|-------|--------|
| Field exists | 3 |
| Length is 1–64 characters | 2 |
| Contains only lowercase letters (a-z), digits (0-9), and hyphens (-) | 2 |
| Does not start or end with a hyphen | 1 |
| Does not contain consecutive hyphens (--) | 1 |
| Matches the parent directory name exactly | 1 |

#### `description` field (10 points)

| Check | Points |
|-------|--------|
| Field exists | 3 |
| Length is 1–1024 characters | 2 |
| Describes WHAT the skill does (not just a label) | 2 |
| Describes WHEN to use it (trigger conditions, use cases) | 2 |
| Contains specific trigger keywords (not just generic terms) | 1 |

**Warning (not a point deduction, but flag it):** If description is under 50 characters, it's almost certainly too vague. If it's over 800 characters, it may be too long for efficient triggering.

#### `license` field (3 points, optional)

| Check | Points |
|-------|--------|
| If present: value is a recognizable license name or references a bundled file | 2 |
| If present: format is concise (not a full license text inline) | 1 |

If absent: award 3 points (it's optional, absence is fine).

#### `compatibility` field (3 points, optional)

| Check | Points |
|-------|--------|
| If present: length is 1–500 characters | 1 |
| If present: describes actual environment requirements (not just "works everywhere") | 2 |

If absent: award 3 points (most skills don't need it).

#### `metadata` field (2 points, optional)

| Check | Points |
|-------|--------|
| If present: is a valid key-value mapping (not a list or scalar) | 1 |
| If present: keys are reasonably unique/namespaced | 1 |

If absent: award 2 points.

#### `allowed-tools` field (2 points, optional)

| Check | Points |
|-------|--------|
| If present: is a space-delimited list of tool names | 1 |
| If present: tool names follow expected format (e.g., `Bash(git:*)`, `Read`) | 1 |

If absent: award 2 points.

### Dimension 3: Body Content Quality (25 points)

Read the full Markdown body (everything after the frontmatter `---`).

| Check | Points | Guidance |
|-------|--------|----------|
| Body has substantive content (not empty or just a title) | 5 | At least a few paragraphs of real instructions |
| Body is under 500 lines | 5 | 500 lines = full score; 500–600 = -2; 600–800 = -4; 800+ = 0 |
| Includes step-by-step instructions or a clear workflow | 5 | Not just a description of what the skill is |
| Uses imperative form ("Do X", "Run Y", "Check Z") | 3 | Passive or descriptive writing is weaker |
| Explains the "why" behind key instructions | 3 | Not just "MUST do X" but "Do X because Y" |
| Defines output format clearly (template, example, or schema) | 4 | User should know exactly what to expect |

**Imperative form check:** Scan for imperative verbs at the start of instruction sentences (Read, Run, Check, Use, Create, Write, Ensure, Avoid, etc.). If most instructions are passive ("The skill will...", "Claude should..."), flag it.

**Why explanation check:** Look for phrases like "because", "so that", "this helps", "the reason", "this ensures". A skill that only issues commands without rationale is harder for Claude to apply correctly in edge cases.

**All-caps command word check:** Scan for `ALWAYS`, `NEVER`, `MUST`, `DO NOT`, `NEVER EVER` used as standalone commands without explanation. From skill-creator: "If you find yourself writing ALWAYS or NEVER in all caps, or using super rigid structures, that's a yellow flag." A few instances are fine; a pattern of them suggests the skill is relying on brute-force commands instead of helping Claude understand the reasoning. Flag as ⚠️ if you find 3+ all-caps commands per 100 lines without accompanying rationale.

### Dimension 4: Progressive Disclosure Design (15 points)

The spec defines three loading tiers:
- **Metadata** (~100 words): name + description, always in context
- **Instructions** (<500 lines recommended): SKILL.md body, loaded on activation
- **Resources** (unlimited): scripts/, references/, assets/, loaded on demand

| Check | Points | Guidance |
|-------|--------|----------|
| name + description together are concise (~100 words / ~500 characters) | 3 | If description alone is 150+ words, it's too heavy for metadata |
| SKILL.md body is under 500 lines | 4 | See body scoring above — this is a separate check for architecture |
| Large reference material is in references/ files, not inline in SKILL.md | 4 | If SKILL.md has 200+ line tables or reference docs, they should be in references/ |
| Reusable scripts are in scripts/, not copy-pasted inline in SKILL.md | 4 | If SKILL.md has 50+ line code blocks that could be scripts, flag it |

**Note:** A skill with no references/ or scripts/ can still score full points here if SKILL.md is appropriately sized. The question is whether the architecture fits the content.

### Dimension 5: Optional Directory Quality (10 points)

Only score directories that exist. If a directory doesn't exist, award full points for it (absence is fine).

#### scripts/ (3 points, if present)

| Check | Points |
|-------|--------|
| Scripts are self-contained or clearly document their dependencies | 1 |
| Scripts include helpful error messages or --help output | 1 |
| Scripts handle edge cases gracefully (not just happy path) | 1 |

#### references/ (4 points, if present)

| Check | Points |
|-------|--------|
| Each reference file is focused on a single topic | 2 |
| Individual reference files are under 300 lines | 1 |
| Files are clearly referenced from SKILL.md with guidance on when to read them | 1 |

#### assets/ (3 points, if present)

| Check | Points |
|-------|--------|
| Assets are appropriate static resources (templates, images, data files) | 2 |
| Assets are actually referenced or used by the skill | 1 |

### Dimension 6: Description Trigger Optimization (10 points)

The description field is the primary mechanism that determines whether Claude invokes a skill. This dimension evaluates it specifically for triggering effectiveness.

**Pre-check — "when to use" belongs in description, not body:** Before scoring, scan the SKILL.md body for sections titled "When to Use", "Trigger Conditions", "When This Skill Applies", or similar. If you find a dedicated section in the body explaining when to trigger the skill, flag it as ⚠️ Warning. From skill-creator: "All 'when to use' info goes here [in description], not in the body." The body should focus on *how* to do the task, not *when* to invoke the skill. Suggest moving that content into the description field.

| Check | Points | Guidance |
|-------|--------|----------|
| Explicitly states when to use the skill (trigger conditions) | 3 | "Use when...", "Trigger when...", "TRIGGER when..." |
| Contains diverse trigger keywords covering different phrasings | 3 | Not just one way to ask, but multiple synonyms and contexts |
| Avoids being too broad (would trigger on unrelated tasks) | 2 | "Use for everything" is as bad as "Use for nothing" |
| Has appropriate "pushiness" to prevent undertriggering | 2 | The spec notes Claude tends to undertrigger; descriptions should be slightly assertive |

**Pushiness check:** Compare these two descriptions:
- Weak: "Helps with PDF files."
- Strong: "Extracts text, fills forms, and merges PDFs. Use whenever the user mentions PDFs, forms, document extraction, or needs to work with PDF content — even if they don't explicitly say 'PDF skill'."

The strong version is more likely to trigger correctly.

---

## Scoring Summary

After scoring all dimensions, calculate the total and assign a grade:

| Score | Grade | Meaning |
|-------|-------|---------|
| 90–100 | Excellent | Fully compliant, production-ready |
| 75–89 | Good | Minor improvements recommended |
| 60–74 | Acceptable | Needs improvement before publishing |
| 40–59 | Poor | Significant issues, rework required |
| 0–39 | Critical | Does not meet spec, major rewrite needed |

---

## Report Format

Generate the report in this exact format. Fill in every section — do not skip sections even if there's nothing to report (write "None found." instead).

```markdown
# Skill Validator Report

## Overview
- **Skill path**: [path or URL provided]
- **Directory name**: [actual directory name]
- **Files found**: [list all files]
- **Validation date**: [current date]
- **Total score**: [X]/100 — [Grade]

## Score Summary

| Dimension | Score | Max | Status |
|-----------|-------|-----|--------|
| 1. Directory Structure | X | 10 | ✅/⚠️/❌ |
| 2. Frontmatter Compliance | X | 30 | ✅/⚠️/❌ |
| 3. Body Content Quality | X | 25 | ✅/⚠️/❌ |
| 4. Progressive Disclosure | X | 15 | ✅/⚠️/❌ |
| 5. Optional Directory Quality | X | 10 | ✅/⚠️/❌ |
| 6. Description Trigger Optimization | X | 10 | ✅/⚠️/❌ |
| **Total** | **X** | **100** | |

> Status key: ✅ ≥ 80% of max points | ⚠️ 50–79% | ❌ < 50%

## Detailed Findings

### Dimension 1: Directory Structure

**Score: X/10**

✅ **Passes:**
- [specific finding with evidence]

⚠️ **Warnings:**
- [specific finding with evidence]

❌ **Failures:**
- [specific finding with evidence]

### Dimension 2: Frontmatter Compliance

**Score: X/30**

#### name field (X/10)
✅ / ⚠️ / ❌ [finding with quoted value]

#### description field (X/10)
✅ / ⚠️ / ❌ [finding with quoted value or excerpt]

#### license field (X/3)
✅ / ⚠️ / ❌ [finding]

#### compatibility field (X/3)
✅ / ⚠️ / ❌ [finding]

#### metadata field (X/2)
✅ / ⚠️ / ❌ [finding]

#### allowed-tools field (X/2)
✅ / ⚠️ / ❌ [finding]

### Dimension 3: Body Content Quality

**Score: X/25**

✅ **Passes:**
- [specific finding]

⚠️ **Warnings:**
- [specific finding]

❌ **Failures:**
- [specific finding]

### Dimension 4: Progressive Disclosure Design

**Score: X/15**

[findings per check]

### Dimension 5: Optional Directory Quality

**Score: X/10**

[findings per directory, or "No optional directories present — full points awarded."]

### Dimension 6: Description Trigger Optimization

**Score: X/10**

[findings with quoted description excerpts]

---

## Improvement Suggestions

### 🔴 High Priority (Must Fix)
These issues violate the spec or critically impact skill functionality:

1. **[Issue name]**: [What's wrong] → [Exact fix with example]

### 🟡 Medium Priority (Should Fix)
These issues reduce skill quality and triggering reliability:

1. **[Issue name]**: [What's wrong] → [Suggested improvement]

### 🟢 Low Priority (Nice to Have)
These are optimizations that would make the skill more robust:

1. **[Issue name]**: [What's wrong] → [Optional improvement]

---

## Quick Fix Checklist

- [ ] [Most critical fix]
- [ ] [Second most critical fix]
- [ ] [Third most critical fix]
- [ ] [Additional fixes as needed]

---

## Reference
- [Agent Skills Specification](https://agentskills.io/specification)
- [anthropics/skills repository](https://github.com/anthropics/skills)
- [Creating Custom Skills](https://support.claude.com/en/articles/12512198-creating-custom-skills)
```

---

## Approach and Mindset

The goal of this validation is to help skill authors improve their work, not to penalize them. Keep this in mind as you apply the scoring rubric.

**Read everything before scoring.** The reason to read every file — not just SKILL.md — is that a skill's quality often shows up in its scripts and reference files. A SKILL.md that looks thin might be appropriately thin because the complexity lives in well-organized references/. Conversely, a long SKILL.md might be hiding content that should have been split out. You can't judge the architecture without seeing all the pieces.

**Quote specific evidence.** Vague feedback like "the description could be better" doesn't help anyone. When you write "The description is 347 characters, includes 'when to use' guidance, and contains trigger keywords: 'PDF', 'forms', 'document extraction'" — that's actionable. The author knows exactly what they did right and can apply the same pattern elsewhere.

**For every failure, show what right looks like.** Don't just identify the problem — provide a concrete example of the fix. This is the difference between a report that gets filed away and one that gets acted on.

**Handle edge cases gracefully:**
- If the skill is a single SKILL.md file with no directory: note this, score what you can, and explain what a full directory structure would add
- If the skill is a complex multi-directory repository: check each skill subdirectory separately if there are multiple
- If you can't access a file: note it as "unable to read" and explain why, then score conservatively
- If the frontmatter is malformed YAML: flag it as a critical failure and attempt to parse what you can

**Composite skills:** Some repositories contain multiple skills (e.g., `skills/pdf/`, `skills/docx/`). Validate each skill separately and provide a combined summary at the end — each skill stands on its own.
