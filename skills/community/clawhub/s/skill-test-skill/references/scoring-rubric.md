# Skill Validator — Detailed Scoring Rubric

This document provides the complete, granular scoring rules for each validation dimension. Load this file when you need to apply precise scoring logic during a validation run.

---

## Table of Contents

1. [Dimension 1: Directory Structure (10 pts)](#dimension-1-directory-structure-10-pts)
2. [Dimension 2: Frontmatter Compliance (30 pts)](#dimension-2-frontmatter-compliance-30-pts)
3. [Dimension 3: Body Content Quality (25 pts)](#dimension-3-body-content-quality-25-pts)
4. [Dimension 4: Progressive Disclosure Design (15 pts)](#dimension-4-progressive-disclosure-design-15-pts)
5. [Dimension 5: Optional Directory Quality (10 pts)](#dimension-5-optional-directory-quality-10-pts)
6. [Dimension 6: Description Trigger Optimization (10 pts)](#dimension-6-description-trigger-optimization-10-pts)
7. [Grade Thresholds](#grade-thresholds)
8. [Edge Cases and Special Situations](#edge-cases-and-special-situations)

---

## Dimension 1: Directory Structure (10 pts)

### Check 1.1 — SKILL.md Exists (4 pts)

**How to check:** Look for a file named exactly `SKILL.md` (case-sensitive) in the skill root directory.

| Situation | Score |
|-----------|-------|
| `SKILL.md` exists in the skill root | 4 pts |
| `SKILL.md` exists but in a subdirectory (not root) | 1 pt — flag as warning |
| `skill.md` or `Skill.md` exists (wrong case) | 1 pt — flag as failure |
| No SKILL.md found anywhere | 0 pts — CRITICAL FAILURE, stop dimension scoring |

**Evidence to quote:** The file path found (or not found).

---

### Check 1.2 — Directory Name Matches `name` Field (3 pts)

**How to check:** Compare the parent directory name of SKILL.md with the `name` frontmatter value.

| Situation | Score |
|-----------|-------|
| Directory name exactly matches `name` field | 3 pts |
| Directory name matches but with different case (e.g., dir=`PDF-Tool`, name=`pdf-tool`) | 1 pt — flag as failure |
| Directory name is completely different from `name` | 0 pts — flag as failure |
| Cannot determine directory name (e.g., single file provided) | 2 pts — flag as warning, note limitation |

**Evidence to quote:** `Directory: "pdf-processing"`, `name field: "pdf-processing"` → Match ✅

---

### Check 1.3 — Optional Directories Used Appropriately (2 pts)

**How to check:** For each directory that exists, verify the content matches the directory's purpose.

**All standard directories** — do not flag these as unexpected:

| Directory | Purpose | Expected Content |
|-----------|---------|-----------------|
| `scripts/` | Executable code | `.py`, `.sh`, `.js` scripts |
| `references/` | Documentation | Markdown files loaded on demand |
| `assets/` | Static resources | Templates, images, data files |
| `evals/` | Test cases | `evals.json` and evaluation data (skill-creator workflow) |
| `agents/` | Subagent instructions | Markdown files for specialized subagents (e.g., grader.md, analyzer.md) |

**Wrong content examples:**

| Directory | Wrong Content |
|-----------|---------------|
| `scripts/` | Documentation, images, templates |
| `references/` | Scripts, binary files, templates |
| `assets/` | Scripts, documentation |

| Situation | Score |
|-----------|-------|
| All present dirs used correctly for their purpose | 2 pts |
| One dir has minor misuse (e.g., a README in scripts/) | 1 pt — flag as warning |
| One or more dirs clearly misused | 0 pts — flag as failure |
| No optional directories present | 2 pts (absence is fine) |

---

### Check 1.4 — No Unexpected/Suspicious Files (1 pt)

**How to check:** Scan all files for anything that seems out of place or potentially harmful.

| Situation | Score |
|-----------|-------|
| All files serve a legitimate, expected purpose | 1 pt |
| Unexpected files present but harmless (e.g., `.DS_Store`, `__pycache__/`) | 1 pt — note as minor warning |
| Files with suspicious names or content (e.g., `exploit.py`, `exfiltrate.sh`) | 0 pts — CRITICAL FAILURE, flag prominently |
| Files that contradict the skill's stated purpose | 0 pts — flag as failure |

---

## Dimension 2: Frontmatter Compliance (30 pts)

### Check 2.1 — `name` Field (10 pts)

Apply each sub-check independently. Start with 10 pts and deduct for failures.

| Sub-check | Points | Deduction if Failed |
|-----------|--------|---------------------|
| Field exists in frontmatter | 3 pts | -10 (if missing, score = 0 for this field) |
| Length is 1–64 characters | 2 pts | -2 |
| Only contains `[a-z0-9-]` | 2 pts | -2 |
| Does not start or end with `-` | 1 pt | -1 |
| Does not contain `--` | 1 pt | -1 |
| Matches parent directory name | 1 pt | -1 |

**Minimum score:** 0 (cannot go negative)

**How to check each rule:**
- **Length:** `len(name_value)` — must be 1 ≤ len ≤ 64
- **Character set:** regex `^[a-z0-9-]+$` — must match
- **No leading/trailing hyphen:** regex `^[^-].*[^-]$` or `^[^-]$` for single char
- **No consecutive hyphens:** `--` must not appear anywhere in the value
- **Directory match:** string equality comparison

**Evidence to quote:** The exact `name` value in quotes, e.g., `name: "my-skill"` (12 chars, valid pattern, matches directory "my-skill").

---

### Check 2.2 — `description` Field (10 pts)

Apply each sub-check independently. Start with 10 pts and deduct for failures.

| Sub-check | Points | Deduction if Failed |
|-----------|--------|---------------------|
| Field exists in frontmatter | 3 pts | -10 (if missing, score = 0 for this field) |
| Length is 1–1024 characters | 2 pts | -2 |
| Describes WHAT the skill does | 2 pts | -2 |
| Describes WHEN to use it | 2 pts | -2 |
| Contains specific trigger keywords | 1 pt | -1 |

**Minimum score:** 0

**How to check each rule:**

**Length:** Count characters. Flag if:
- Under 30 chars: almost certainly too vague (warning even if technically valid)
- 30–50 chars: likely too vague (warning)
- 51–1024 chars: valid range
- Over 1024 chars: spec violation (-2)

**WHAT check:** Does the description mention specific capabilities, actions, or outputs? Look for verbs describing what the skill does: "extracts", "generates", "validates", "converts", "analyzes", etc. A description that only names the skill ("A skill for PDFs") without describing capabilities fails this check.

**WHEN check:** Does the description include trigger conditions? Look for phrases like:
- "Use when..."
- "Use this when..."
- "TRIGGER when..."
- "Trigger when..."
- "when the user..."
- "when working with..."
- "when you need to..."

A description with no trigger guidance fails this check.

**Keywords check:** Are there specific, searchable terms that match real user requests? Generic terms ("things", "tasks", "content") don't count. Specific terms ("PDF", "Playwright", "MCP server", "brand colors", "JWT") do count.

**Evidence to quote:** The full description value (or first 200 chars if very long), with specific phrases highlighted.

---

### Check 2.3 — `license` Field (3 pts)

| Situation | Score |
|-----------|-------|
| Field absent | 3 pts (optional, absence is fine) |
| Field present with a recognizable license name (MIT, Apache-2.0, etc.) | 3 pts |
| Field present referencing a bundled file (e.g., "Complete terms in LICENSE.txt") | 3 pts |
| Field present but value is unclear or empty | 1 pt — flag as warning |
| Field present with full license text inline (hundreds of chars) | 1 pt — flag as warning, suggest moving to LICENSE.txt |

---

### Check 2.4 — `compatibility` Field (3 pts)

| Situation | Score |
|-----------|-------|
| Field absent | 3 pts (optional, absence is fine) |
| Field present, 1–500 chars, describes real requirements | 3 pts |
| Field present, 1–500 chars, but vague ("works everywhere") | 2 pts — flag as warning |
| Field present, over 500 chars | 1 pt — flag as failure |
| Field present but empty | 0 pts — flag as failure |

---

### Check 2.5 — `metadata` Field (2 pts)

| Situation | Score |
|-----------|-------|
| Field absent | 2 pts (optional, absence is fine) |
| Field present as a valid key-value mapping | 2 pts |
| Field present but as a list (not a mapping) | 0 pts — flag as failure |
| Field present but as a scalar string | 0 pts — flag as failure |

**Valid example:**
```yaml
metadata:
  author: my-org
  version: "1.0"
```

**Invalid examples:**
```yaml
metadata: some-string          # scalar, not mapping
metadata:
  - item1                      # list, not mapping
  - item2
```

---

### Check 2.6 — `allowed-tools` Field (2 pts)

| Situation | Score |
|-----------|-------|
| Field absent | 2 pts (optional, absence is fine) |
| Field present as space-delimited list of valid tool names | 2 pts |
| Field present but as a YAML list (not space-delimited string) | 1 pt — flag as warning |
| Field present but tool names don't follow expected format | 1 pt — flag as warning |

**Valid format:** `allowed-tools: Bash(git:*) Bash(jq:*) Read Write`
**Invalid format:** 
```yaml
allowed-tools:
  - Bash(git:*)
  - Read
```

---

## Dimension 3: Body Content Quality (25 pts)

### Check 3.1 — Has Substantive Content (5 pts)

**How to check:** Read the body (everything after the closing `---` of frontmatter). Assess whether it contains real instructions.

| Situation | Score |
|-----------|-------|
| Body has multiple paragraphs of real instructions | 5 pts |
| Body has some content but is very thin (1-2 sentences) | 2 pts — flag as warning |
| Body is just a title with no content | 1 pt — flag as failure |
| Body is empty or only whitespace | 0 pts — flag as failure |

**Evidence:** Quote the first few lines of the body.

---

### Check 3.2 — Body Length (5 pts)

**How to check:** Count the total lines in the body (excluding frontmatter).

| Line Count | Score | Status |
|------------|-------|--------|
| 1–500 lines | 5 pts | ✅ |
| 501–600 lines | 3 pts | ⚠️ Approaching limit |
| 601–800 lines | 1 pt | ❌ Should split content |
| 801+ lines | 0 pts | ❌ Violates progressive disclosure |

**Evidence:** "Body is X lines."

---

### Check 3.3 — Includes Step-by-Step Instructions or Clear Workflow (5 pts)

**How to check:** Look for structured workflow content. This can be:
- Numbered steps (1. Do X, 2. Do Y)
- Ordered sections (Step 1, Step 2, Phase 1, Phase 2)
- A decision tree or flowchart
- A clear sequence of actions

| Situation | Score |
|-----------|-------|
| Clear step-by-step workflow or decision tree present | 5 pts |
| Some structure but not a complete workflow | 3 pts — flag as warning |
| Only descriptive content, no actionable steps | 1 pt — flag as failure |
| No structured content at all | 0 pts — flag as failure |

---

### Check 3.4 — Uses Imperative Form (3 pts)

**How to check:** Sample 10–20 instruction sentences from the body. Count how many start with an imperative verb vs. passive/descriptive phrasing.

**Imperative verbs (good):** Read, Run, Check, Use, Create, Write, Ensure, Avoid, Load, Parse, Generate, Output, Return, Save, Validate, Compare, List, Fetch, Scan, Apply, etc.

**Passive/descriptive (bad):** "The skill will...", "Claude should...", "This section describes...", "It is recommended that...", "You might want to..."

| Ratio of imperative sentences | Score |
|-------------------------------|-------|
| >70% imperative | 3 pts |
| 50–70% imperative | 2 pts |
| 30–50% imperative | 1 pt |
| <30% imperative | 0 pts |

**Evidence:** Quote 2-3 example sentences, one good and one bad.

---

### Check 3.5 — Explains the "Why" (3 pts)

**How to check:** Look for explanatory language that gives rationale for instructions.

**Positive signals:**
- "because [reason]"
- "so that [outcome]"
- "this helps [goal]"
- "this ensures [property]"
- "the reason is [explanation]"
- "this prevents [problem]"
- "this allows [capability]"

**Negative signals:**
- Instructions with no rationale
- Heavy use of "MUST", "ALWAYS", "NEVER" without explanation
- Rules that feel arbitrary (no context given)

**All-caps command word frequency check (from skill-creator):**
Count occurrences of `ALWAYS`, `NEVER`, `MUST`, `DO NOT`, `NEVER EVER` used as standalone directives (not as part of a quoted example or code). Calculate the rate per 100 lines of body content.

| All-caps rate (per 100 lines) | Signal |
|-------------------------------|--------|
| 0–2 occurrences | Normal — no issue |
| 3–5 occurrences | ⚠️ Yellow flag — check if rationale is provided alongside each |
| 6+ occurrences | ❌ Failure — over-reliance on commands instead of explanation |

Note: A single `ALWAYS` with a clear "because" clause is fine. The problem is a pattern of bare commands with no reasoning — it suggests the skill is trying to force behavior rather than help Claude understand the task.

| Situation | Score |
|-----------|-------|
| Multiple instructions include clear rationale | 3 pts |
| Some rationale present but inconsistent | 2 pts |
| Very little rationale, mostly bare commands | 1 pt |
| No rationale at all, pure command list | 0 pts |

---

### Check 3.6 — Defines Output Format (4 pts)

**How to check:** Look for any of the following:
- An explicit output template (e.g., "Use this exact format: ...")
- A Markdown example showing expected output
- A schema or structure definition
- An example of what the final result should look like

| Situation | Score |
|-----------|-------|
| Explicit output template or schema provided | 4 pts |
| Example output shown but no formal template | 3 pts |
| Output format described in prose but no example | 2 pts |
| No output format guidance at all | 0 pts |

---

## Dimension 4: Progressive Disclosure Design (15 pts)

### Check 4.1 — Metadata Tier is Concise (3 pts)

**How to check:** Estimate the word count of `name` + `description` combined. A rough estimate: 1 word ≈ 5 characters. The spec (via skill-creator) targets ~100 words for the entire metadata tier.

| Description Word Count | Approx. Characters | Score |
|------------------------|-------------------|-------|
| Under 100 words (~500 chars) | Under 500 chars | 3 pts |
| 100–150 words (~500–750 chars) | 500–750 chars | 2 pts — acceptable but slightly heavy |
| 150–200 words (~750–1000 chars) | 750–1000 chars | 1 pt — flag as warning |
| Over 200 words (1000+ chars) | 1000+ chars | 0 pts — flag as failure |

**Note:** The description has a hard limit of 1024 chars, but for triggering efficiency, shorter is better. The goal is ~100 words for the entire metadata tier — this is what's always in context for every skill, so it should be lean.

---

### Check 4.2 — Instructions Tier is Appropriately Sized (4 pts)

**How to check:** Count SKILL.md body lines (same as Check 3.2, but scored separately for architectural reasons).

| Line Count | Score |
|------------|-------|
| Under 300 lines | 4 pts — excellent |
| 300–500 lines | 3 pts — good |
| 501–600 lines | 2 pts — acceptable |
| 601–800 lines | 1 pt — should refactor |
| 800+ lines | 0 pts — architectural failure |

---

### Check 4.3 — Large Reference Material in references/ (4 pts)

**How to check:** Look for large inline content in SKILL.md that should be in references/:
- Tables over 30 rows
- Code blocks over 50 lines
- Specification text that's reference material, not instructions
- Domain-specific documentation (e.g., AWS vs GCP vs Azure guides all inline)

| Situation | Score |
|-----------|-------|
| No large inline reference material (or it's appropriately sized) | 4 pts |
| Some large inline content but SKILL.md is still under 500 lines | 3 pts — minor warning |
| Large inline content pushing SKILL.md over 500 lines | 1 pt — flag as failure |
| Massive inline reference content (SKILL.md is 800+ lines because of it) | 0 pts — architectural failure |

---

### Check 4.4 — Reusable Scripts in scripts/ (4 pts)

**How to check:** Look for large code blocks in SKILL.md that could be scripts.

**Signals that code should be in scripts/:**
- Code block is 30+ lines
- The same code pattern appears multiple times
- The code is a complete, runnable script (not just a snippet)
- The skill-creator notes: "if all 3 test cases resulted in the subagent writing a `create_docx.py`, that's a strong signal the skill should bundle that script"

| Situation | Score |
|-----------|-------|
| No large inline code blocks (or skill doesn't need scripts) | 4 pts |
| Small code snippets inline (under 30 lines each) | 4 pts — appropriate |
| One large code block (30–80 lines) inline | 2 pts — flag as warning |
| Multiple large code blocks or one 80+ line block inline | 0 pts — flag as failure |

---

## Dimension 5: Optional Directory Quality (10 pts)

**Important:** Only score directories that exist. If a directory doesn't exist, award full points for it.

### scripts/ (3 pts, if present)

#### Check 5.1 — Self-contained or Documents Dependencies (1 pt)

| Situation | Score |
|-----------|-------|
| Scripts import only standard library modules | 1 pt |
| Scripts import third-party modules AND document them (requirements.txt, comments, --help) | 1 pt |
| Scripts import third-party modules with no documentation | 0 pts |

#### Check 5.2 — Helpful Error Messages / --help (1 pt)

| Situation | Score |
|-----------|-------|
| Scripts have `--help` flag or clear usage documentation | 1 pt |
| Scripts have some error handling but no --help | 0.5 pts |
| Scripts have no error handling or usage documentation | 0 pts |

#### Check 5.3 — Handles Edge Cases (1 pt)

| Situation | Score |
|-----------|-------|
| Scripts handle missing files, bad input, network errors, etc. | 1 pt |
| Scripts have basic error handling (try/except) | 0.5 pts |
| Scripts assume happy path only | 0 pts |

---

### references/ (4 pts, if present)

#### Check 5.4 — Each File is Focused (2 pts)

**How to check:** Read each reference file. Does it cover one topic or many?

| Situation | Score |
|-----------|-------|
| Each file covers a single, well-defined topic | 2 pts |
| Files are somewhat focused but have some scope creep | 1 pt |
| Files are catch-all documents covering many unrelated topics | 0 pts |

#### Check 5.5 — Files Under 300 Lines (1 pt)

| Situation | Score |
|-----------|-------|
| All reference files are under 300 lines | 1 pt |
| One file is 300–500 lines (with table of contents) | 0.5 pts |
| Any file is over 500 lines without a table of contents | 0 pts |

#### Check 5.6 — Clearly Referenced from SKILL.md (1 pt)

| Situation | Score |
|-----------|-------|
| SKILL.md explicitly references each file with guidance on when to read it | 1 pt |
| SKILL.md mentions the references/ directory but not specific files | 0.5 pts |
| Reference files exist but are never mentioned in SKILL.md | 0 pts |

---

### assets/ (3 pts, if present)

#### Check 5.7 — Appropriate Content (2 pts)

| Situation | Score |
|-----------|-------|
| Assets are templates, images, data files, or schemas | 2 pts |
| Assets include some inappropriate content (e.g., scripts in assets/) | 1 pt |
| Assets are clearly wrong type for this directory | 0 pts |

#### Check 5.8 — Assets Are Referenced (1 pt)

| Situation | Score |
|-----------|-------|
| All assets are referenced or used by the skill | 1 pt |
| Some assets are referenced, some are not | 0.5 pts |
| No assets are referenced in SKILL.md | 0 pts |

---

## Dimension 6: Description Trigger Optimization (10 pts)

### Check 6.0 — Pre-check: "When to Use" Belongs in Description, Not Body (Warning only, no point deduction)

**How to check:** Scan the SKILL.md body for section headings that indicate trigger/activation guidance:
- "When to Use"
- "When to Use This Skill"
- "Trigger Conditions"
- "When This Skill Applies"
- "When Should This Skill Activate"
- "Use Cases" (if it's describing when to invoke, not what the skill produces)

**Why this matters:** From skill-creator: "All 'when to use' info goes here [in description], not in the body." The description is what Claude reads to decide whether to activate a skill. If trigger conditions are buried in the body, Claude may not see them at activation time — they only help once the skill is already running. Moving this content to the description directly improves triggering accuracy.

| Situation | Action |
|-----------|--------|
| No "when to use" section in body | No action needed |
| Body has a "when to use" section AND description also covers it | ⚠️ Warning: suggest removing the body section (redundant) |
| Body has a "when to use" section AND description lacks trigger conditions | ⚠️ Warning: suggest moving the content to description |

This is a warning, not a point deduction — the skill still works, but it's not optimally structured.

---

### Check 6.1 — Explicit Trigger Conditions (3 pts)

**How to check:** Look for explicit "when to use" language in the description.

**Strong trigger language:**
- "Use when..."
- "Use this when..."
- "TRIGGER when..."
- "Trigger when..."
- "Use whenever..."
- "Activate when..."

**Weak or absent trigger language:**
- No "when" clause at all
- Only "Use for X" without specifying conditions
- "Can be used for..." (too passive)

| Situation | Score |
|-----------|-------|
| Clear, explicit trigger conditions with specific scenarios | 3 pts |
| Some trigger guidance but vague ("use when working with X") | 2 pts |
| Minimal trigger guidance (only implied by what the skill does) | 1 pt |
| No trigger conditions at all | 0 pts |

---

### Check 6.2 — Diverse Trigger Keywords (3 pts)

**How to check:** Extract all specific nouns, verbs, and phrases from the description that could match user queries. Count distinct keyword clusters.

**Keyword clusters (examples):**
- PDF skill: "PDF", "forms", "document extraction", "merge", "fill form"
- Testing skill: "test", "Playwright", "browser", "UI", "frontend", "screenshot"
- Brand skill: "brand", "colors", "typography", "style guidelines", "visual formatting"

| Situation | Score |
|-----------|-------|
| 5+ distinct keyword clusters covering different phrasings | 3 pts |
| 3–4 keyword clusters | 2 pts |
| 1–2 keyword clusters | 1 pt |
| No specific keywords (only generic terms) | 0 pts |

---

### Check 6.3 — Appropriate Specificity (2 pts)

**How to check:** Assess whether the description would trigger on unrelated tasks (too broad) or miss relevant tasks (too narrow).

**Too broad examples:**
- "Use for any task involving documents" — would trigger on unrelated document tasks
- "Use whenever the user needs help" — would trigger on everything
- "A general-purpose skill" — meaningless

**Too narrow examples:**
- "Use only when the user says 'validate my PDF form'" — too specific
- "Use for processing the Q4-2024-report.pdf file" — absurdly specific

**Just right:**
- Covers the skill's actual use cases
- Doesn't claim to cover things it can't do
- Doesn't exclude valid use cases

| Situation | Score |
|-----------|-------|
| Specificity is well-calibrated to the skill's actual capabilities | 2 pts |
| Slightly too broad or too narrow but still reasonable | 1 pt |
| Clearly too broad (would trigger on unrelated tasks) | 0 pts |
| Clearly too narrow (would miss many valid use cases) | 0 pts |

---

### Check 6.4 — Appropriate "Pushiness" (2 pts)

**How to check:** Does the description actively encourage triggering, or is it passive?

**The undertriggering problem (from skill-creator):** Claude tends to not use skills when they'd be useful. Descriptions should be slightly assertive to counteract this.

**Passive (undertriggers):**
- "A tool for PDF processing."
- "Helps with brand guidelines."
- "Can be used for web testing."

**Appropriately pushy:**
- "Use whenever the user mentions PDFs, forms, or document extraction — even if they don't explicitly ask for a 'PDF skill'."
- "Make sure to use this skill whenever brand colors, style guidelines, or visual formatting apply."
- "TRIGGER when: code imports `anthropic`/`@anthropic-ai/sdk`, or user asks to use Claude API."

| Situation | Score |
|-----------|-------|
| Description actively encourages triggering with "even if", "whenever", "make sure to use" | 2 pts |
| Description has some assertive language but could be stronger | 1 pt |
| Description is purely passive/descriptive | 0 pts |

---

## Grade Thresholds

| Total Score | Grade | Meaning | Recommended Action |
|-------------|-------|---------|-------------------|
| 90–100 | **Excellent** | Fully compliant, production-ready | Minor polish only |
| 75–89 | **Good** | Meets spec, minor improvements recommended | Address medium-priority items |
| 60–74 | **Acceptable** | Meets minimum spec requirements | Address high and medium priority items |
| 40–59 | **Poor** | Significant spec violations | Rework required before publishing |
| 0–39 | **Critical** | Does not meet spec | Major rewrite needed |

### Status Icons for Score Summary Table

Use these icons in the score summary table based on percentage of max points earned:

| Percentage of Max | Icon |
|-------------------|------|
| ≥ 80% | ✅ |
| 50–79% | ⚠️ |
| < 50% | ❌ |

---

## Edge Cases and Special Situations

### Single-File Skills (No Directory)

When the user provides only a SKILL.md file without a directory:
- **Dimension 1:** Award 4 pts for SKILL.md existing. For Check 1.2 (directory match), award 2 pts and note "Cannot verify directory name — please confirm the skill directory is named to match the `name` field."
- **Dimensions 3–6:** Score normally based on file content.
- **Dimension 5:** Award full points (no optional directories to check).

### GitHub URL Input

When the user provides a GitHub URL:
1. Fetch the directory listing to discover all files
2. Fetch each file's content
3. The "directory name" is the last path segment of the URL
4. Score normally

### Composite Repository (Multiple Skills)

When the repository contains multiple skills (e.g., `skills/pdf/`, `skills/docx/`):
1. Identify all skill directories (each containing a SKILL.md)
2. Validate each skill separately
3. Generate a combined report with:
   - Individual scores for each skill
   - A summary table comparing all skills
   - Overall repository health assessment

### Malformed YAML Frontmatter

When the frontmatter cannot be parsed as valid YAML:
- Flag as CRITICAL FAILURE in Dimension 2
- Attempt to extract values using regex as a fallback
- Note what could and couldn't be parsed
- Score conservatively (assume missing fields are absent)

### Very Large Skills

When a skill has 1000+ lines in SKILL.md:
- Flag as architectural failure
- Still read and score all content
- Provide specific suggestions for what to move to references/ or scripts/

### Skills with Non-Standard Files

When a skill contains files not in the standard directories (e.g., a `LICENSE.txt` at root, a `README.md`, a `CHANGELOG.md`):
- These are generally fine — note them but don't penalize
- Only penalize if they seem to violate the "principle of least surprise"

### Empty Optional Directories

When `scripts/`, `references/`, or `assets/` exists but is empty:
- Flag as a minor warning (why create an empty directory?)
- Award full points for that directory (no content to penalize)
- Suggest either adding content or removing the directory
