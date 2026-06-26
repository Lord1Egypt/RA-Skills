# Skill Writer

Create well-structured Agent Skills for Claude Code with proper validation.

## When to Use

- Creating a new Agent Skill
- Writing or updating SKILL.md files
- Converting existing prompts/workflows into Skills
- Troubleshooting skill discovery issues

## Instructions

### Step 1: Determine Skill Scope

Ask clarifying questions:
- What specific capability should this Skill provide?
- When should Claude use this Skill?
- What tools or resources does it need?
- Is this for personal use or team sharing?

**Keep it focused**: One Skill = one capability
- Good: "PDF form filling", "Excel data analysis"
- Too broad: "Document processing", "Data tools"

**Language rule**: Skills intended for distribution (ClawHub, plugins) must be written in **English** — SKILL.md frontmatter, headings, and body. Personal-only skills may use any language.

**Description field language rule**: The `description` frontmatter field (including trigger keywords) must match the skill's language. If the skill is English, **all trigger keywords must be English** — no Korean mixed in. This applies to both new skills and upgrades.

### Step 2: Choose Location

| Location | Purpose |
|----------|---------|
| `~/.claude/skills/` | Personal skills |
| `.claude/skills/` | Project skills (committed to git) |

### Step 3: Create Structure

```bash
mkdir -p ~/.claude/skills/skill-name
```

For multi-file Skills:
```
skill-name/
├── SKILL.md (required)
├── reference.md (optional)
├── examples.md (optional)
└── scripts/ (optional)
```

For multi-topic Skills, see [architecture.md](./architecture.md).

### Step 3.5: Detect Language

When adding topics to an existing skill, match the language of the existing content:

1. Read the existing `SKILL.md` and 1-2 topic files
2. If content is **English** → write new topic in **English only**
3. If content is **Korean** → write in **Korean** (technical terms in English OK)
4. If mixed → follow the **majority language**

**Do not** write Korean content in an English skill or vice versa.

### Step 4: Write Frontmatter

```yaml
---
name: skill-name
description: Brief description of what this does and when to use it
---
```

**Field requirements**:

- **name**: lowercase, hyphens only, max 64 chars, must match directory name
- **description**: **max 1024 chars (HARD STOP — Claude Code truncates excess with `…`, dropping tail trigger keywords).** Include "what" AND "when to use". Measure before saving: `awk '/^description:/,/^---$/' SKILL.md | sed -E 's/^description: //; /^---$/d' | tr -d '\n' | wc -c`. See `lint.md` "Description Length Budget" for reduction strategies if approaching limit.

**Optional fields**:
```yaml
allowed-tools: [Read, Grep, Glob]  # Restrict tool access
model: claude-sonnet-4-...         # Specific model
context: fork                       # Context handling
```

### Step 5: Write Effective Descriptions

**No `<example>` blocks**: Do not put `<example>` blocks in SKILL.md frontmatter. `<example>` is agent-only syntax (`.claude/agents/*.md`). Skills match via description text and trigger keywords only.

**Formula**: `[What it does] + [When to use it] + [Key triggers]`

✅ **Good**:
```yaml
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

❌ **Too vague**:
```yaml
description: Helps with documents
```

**Tips**:
- Include specific file extensions (.pdf, .xlsx, .json)
- Mention common user phrases ("analyze", "extract", "generate")
- Add context clues ("Use when...", "For...")

### Step 5.4: Skill body tone — no profanity or slang in always-loaded content (HARD STOP)

Skill files (`SKILL.md`, topic `.md`, rule files in `~/.agents/rules/`) are always loaded into Claude's context. Their tone must remain professional and durable.

**Forbidden in skill/rule body**:
- Direct quotation of user profanity in any language (transliterated explicits, f-word equivalents, etc.)
- User-facing slang reflecting frustration ("did I just get scammed?", "are you serious right now?", etc.)
- Quotation of user anger as "evidence" of a violation case

**Allowed locations for user verbatim text**:
- `~/.claude/skills/cleanup/data/failed-attempts.md` (HOT) — on-demand load, evidence preservation
- `~/.claude/skills/cleanup/data/archive/*.md` — cold storage
- chat messages and one-time analysis artifacts (`.ralph/docs/generated/plan-fix-*.md`)

**Required transformation when adding a violation case to skill body**:

| # | Don't | Do |
|---|-------|-----|
| 1 | Quote user profanity verbatim in a Rules / Anti-pattern bullet | Describe the violation **outcome neutrally**: "user found the option choice produced no actual change" instead of quoting their reaction |
| 2 | Add the user's anger expression as parenthetical "evidence" of severity | Use a numbered case ID (e.g., `(2026-05-24, 2nd recurrence)`) + 1-line factual summary. The verbatim quote lives in failed-attempts.md |
| 3 | Conclude that emotional emphasis belongs in the skill body because "it shows the user really cared" | Severity is conveyed through HARD STOP markers, recurrence count, and self-check enforcement — not through quoting frustration |

**Self-check** (every time before adding a violation case to skill/rule body):

1. Does the case description contain user-quoted profanity or slang? → If yes, remove and replace with a neutral outcome description
2. Does it cite the user's emotional state (frustrated, angry, suspicious)? → If yes, replace with the factual outcome the user observed
3. Is the case ID present (`YYYY-MM-DD, Nth recurrence`)? → Required for traceability
4. If the verbatim quote is essential for forensic context, move it to `failed-attempts.md` and reference it by date from the skill body

**Violation case (2026-05-24, 2nd recurrence)**: A skill body bullet quoted user profanity and frustration slang verbatim as "evidence" of a violation. The user pointed out that skill/rule bodies (always-loaded into context) must not carry profanity in any language. The bullet was rewritten with a neutral outcome description in the same fix. This Step 5.4 was added to prevent recurrence; the verbatim quotes are preserved in `failed-attempts.md` for forensic context.

### Step 5.5: Do & Don't Tables for Behavioral Rules

When the skill contains behavioral constraints (forbidden patterns + correct alternatives), use **Do & Don't table** format instead of prose:

```markdown
| # | Don't (forbidden) | Do (correct alternative) |
|---|-------------------|------------------------|
| 1 | `Bash("cmd1 && cmd2")` | `Bash("cmd1")` then `Bash("cmd2")` |
```

- Pairs of "don't do X / do Y instead" → always table
- 2+ times violated rules → table mandatory
- Simple principle declarations → prose OK

### Step 5.6: Configuration & Portability (distribution skills)

**For skills intended for distribution** (ClawHub, plugins, shared across projects), extract project-specific values into a Configuration section:

| Hardcoded (bad) | Configurable (good) |
|----------------|-------------------|
| `.ralph/docs/generated/` | `{output-dir}` option (default: `docs/generated/`) |
| `pnpm test` | `{test-command}` option (default: auto-detect) |
| `http://localhost:3000` | `{base-url}` option |
| `fix_plan.md` | `{task-tracker}` option |

**Portability checklist** (must pass before publishing):
- [ ] No absolute paths to user directories (`~/.ralph/`, `~/Sync/`)
- [ ] No project-specific tool names (Ralph, fix_plan, Semaphore) without opt-in
- [ ] No hardcoded server URLs or ports
- [ ] All environment-specific values have defaults + override options
- [ ] Topic files use `{option-name}` placeholders, not literal paths

**SKILL.md Configuration section template**:
```markdown
## Configuration

| Option | Default | Description |
|--------|---------|-------------|
| `output-dir` | `docs/generated/` | Directory for generated artifacts |
```

**Personal-only skills may skip this step.**

### Step 6: Structure Content

```markdown
# Skill Name

Brief overview.

## Quick Start

Simple example to get started.

## Instructions

Step-by-step guidance:
1. First step with clear action
2. Second step with expected outcome

## Examples

Concrete usage examples.

## Requirements

Dependencies or prerequisites.

## Requirements

Dependencies or prerequisites.
```

### Step 6.5: Document Topic Dependencies (multi-topic skills)

For skills with multiple topics that depend on each other or on external skills, add a **Topic Dependencies** section to SKILL.md after the Topics table.

```markdown
## Topic Dependencies

\```
skill-name (main workflow)
  └─→ external-skill/topic (used in step N)
  └─→ topic-b (optional: extends main workflow)
        └─→ another-skill (used by topic-b)
\```

- topic-a: always executed
- topic-b: optional, opt-out with `--no-flag`
```

**Rules**:
- Show the execution flow as an ASCII tree
- Mark optional topics explicitly
- Include cross-skill references (e.g., `tdd/cycle` used by `code-workflow` step 4)
- Add opt-out flags where applicable
- Also add referenced skills to the `depends-on` frontmatter field

### Step 7: Validate

Checklist:
- [ ] SKILL.md exists in correct location
- [ ] Directory name matches frontmatter `name`
- [ ] Opening `---` on line 1
- [ ] `name` follows naming rules
- [ ] `description` is specific and < 1024 chars
- [ ] Clear instructions for Claude
- [ ] Concrete examples provided

### Step 8: Test

1. Restart Claude Code to load the Skill
2. Ask relevant questions that match the description
3. Verify activation and behavior

## Common Patterns

### Read-only Skill

```yaml
---
name: code-reader
description: Read and analyze code without changes. Use for code review or documentation.
allowed-tools: [Read, Grep, Glob]
---
```

### Script-based Skill

```yaml
---
name: data-processor
description: Process CSV/JSON data files. Use when analyzing or transforming datasets.
---

## Instructions

1. Run: `python scripts/process.py input.csv`
```

## Troubleshooting

**Skill doesn't activate**:
- Make description more specific with trigger words
- Include file types and operations
- Add "Use when..." clause

**Multiple Skills conflict**:
- Make descriptions more distinct
- Use different trigger words

## Output

When creating a Skill:
1. Ask clarifying questions
2. Suggest name and location
3. Create SKILL.md with proper frontmatter
4. Include instructions and examples
5. Validate against requirements
