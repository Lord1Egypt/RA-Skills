---
name: skill-craft
description: >
  Create, optimize, or update AgentSkills with evidence-based design. Two modes:
  (1) CREATE — build new skills from scratch with proven design patterns.
  (2) OPTIMIZE — diagnose and fix existing skills across 9 evidence-based dimensions:
  trigger precision, context efficiency, structured instructions, step decomposition,
  positive constraints, example design, verification, freedom calibration, progressive loading.
  Based on 25+ peer-reviewed papers (ACL/NeurIPS/EMNLP 2023-2025), Anthropic/Google/Microsoft
  official guides, and Claude Code/Cursor community practices.
  Trigger: "create skill", "optimize skill", "improve skill", "fix skill", "package skill",
  "skill not working", "skill design", "SKILL.md", "写技能", "优化技能",
  "skill type", "skill classification", "state management", "技能分类"
---

# Skill Craft

Build and optimize AI agent skills using evidence-based design principles.

## Two Modes of Operation

**CREATE mode** — Build a new skill from scratch (Steps 1-6).
**OPTIMIZE mode** — Diagnose and fix an existing skill (Step 7).

For new skills, follow Steps 1-6 (Step 7 baked into Step 4). For existing skills needing improvement, jump to Step 7.

---

## Skill Classification

Before creating or optimizing, classify the skill type — this determines design priorities.

### Nine Skill Types

| Type | Code | Definition | Design Priority |
|---|---|---|---|
| Process Control | PROC | Sequential, phased workflows (brainstorming, planning) | D4 Steps → D7 Verify → D2 Efficiency |
| Methodology | METH | Reusable methods with iron laws (TDD, debugging) | D4 Steps → D7 Verify → D5 Positive |
| Tool Integration | TOOL | API/CLI wrappers (web-access, calculator) | D1 Description → D8 Freedom → D6 Examples |
| Domain Knowledge | KNOW | Domain expertise and standards (design, mobile) | D9 Progressive → D2 Efficiency → D3 Structure |
| Creative/Generative | GEN | Creative output with quality bars (prompt refinement) | D5 Positive → D8 Freedom → D6 Examples |
| Document Generation | DOC | Structured document output (reports, wikis) | D4 Steps → D3 Structure → D7 Verify |
| Orchestration | ORCH | Multi-agent/task coordination (parallel dispatch) | D4 Steps → D7 Verify → D6 Examples |
| Meta-Skill | META | Skills about skills (this very skill) | D3 Structure → D9 Progressive → D5 Positive |
| Quality Assurance | QA | Verification and review (code review, testing) | D7 Verify → D5 Positive → D4 Steps |

See `references/skill-taxonomy.md` for per-type design templates, pitfalls, and the full classification decision tree.

---

## Skill Anatomy

```
skill-name/
├── SKILL.md          (required) — YAML frontmatter + Markdown instructions
├── scripts/          (optional) — Deterministic code (Python/Bash)
├── references/       (optional) — Detailed docs loaded on demand
└── assets/           (optional) — Templates/images used in output
```

### Three-Level Loading (Progressive Disclosure)

| Level | Content | When Loaded | Size Target |
|---|---|---|---|
| 1 | `name` + `description` (frontmatter) | Always in context | ~100 words |
| 2 | SKILL.md body | When skill triggers | < 500 lines, < 5k words |
| 3 | `scripts/`, `references/`, `assets/` | On demand | Unlimited |

**Why this matters:** Context window is the scarcest resource. Claude Code Issue #2544 (39👍) proves rules get ignored when SKILL.md is too long. CFPO research (Fudan/Microsoft, 2025) shows format+content joint optimization yields +5~38% improvement.

### What NOT to Include

README.md, CHANGELOG.md, installation guides, user-facing docs. Only what the AI agent needs to do the job.

### State Management in Skills

Some skills need state management — tracking progress across steps or sessions. Based on OpenSpec's DAG pattern and LangGraph's checkpoint system (see `references/state-machine-patterns.md`).

**Does this skill need state management?**

| Condition | Needs State? | Pattern |
|---|---|---|
| Multi-step workflow with dependencies between steps | YES | DAG + file existence checks |
| Output of one step feeds into another | YES | Checkpoint pattern |
| Each invocation is independent | NO | Stateless |
| Free-form exploration or conversation | NO | Stateless |

For state patterns (file existence, checkbox, YAML, DAG) and script integration, see `references/state-machine-patterns.md`.

**Key principle:** Use deterministic checks (file exists, script output) rather than LLM judgment for state transitions. Research (arXiv:2511.07585) shows large models have only 12.5% output consistency — scripts are 8× more reliable.

---

## CREATE Mode: Steps 1-6

### Skill Naming

- Lowercase letters, digits, hyphens only. Under 64 chars.
- Prefer short, verb-led: `pdf-editor`, `db-migrate`, `brand-styling`.
- Namespace by tool when it helps triggering: `gh-address-comments`.

### Step 1: Understand with Concrete Examples

Ask the user (one question at a time):

1. "What should this skill do?"
2. "Can you give 2-3 examples of how it would be used?"
3. "What would a user say that should trigger this skill?"
4. "Are there edge cases or error scenarios to handle?"

### Step 2: Plan Resources

For each example from Step 1, identify reusable components:

| If the task... | Add this resource |
|---|---|
| Rewrites the same code each time | `scripts/transform.py` |
| Requires domain schemas/docs | `references/schema.md` |
| Uses templates or boilerplate | `assets/template/` |

### Step 3: Initialize

```bash
scripts/init_skill.py <skill-name> --path <output-dir> [--resources scripts,references,assets] [--examples]
```

### Step 4: Write the Skill (with Built-in Optimization)

This step creates SKILL.md following all 9 optimization dimensions from the start. Write using imperative form.

#### 4a. Write Frontmatter (D1: Trigger Precision)

The `description` field is the **only content always loaded**. It determines whether the skill triggers at all. Issue #9716 (69👍) documents skills ignored because descriptions lacked trigger phrases.

**Three-part formula:**

```yaml
# BAD — vague, no triggers
description: Helps with PDF operations

# GOOD — capabilities + trigger scenarios + keywords
description: >
  Create, edit, and analyze PDF documents with form filling,
  text extraction, and page manipulation. Use when: (1) Creating PDFs,
  (2) Extracting text or form data, (3) Rotating/merging pages,
  (4) Converting PDFs to images. Trigger: "pdf", "rotate pdf",
  "merge pdf", "extract text", "fill form"
```

Only `name` and `description` fields allowed in frontmatter.

#### 4b. Write Body Sections (D3: Structure)

Separate content types with Markdown headings:

```markdown
## Workflow
[Numbered steps — see D4 below]

## Constraints
[Specific, measurable rules — see D5 below]

## Examples
[Concrete user request → agent behavior — see D6 below]

## Verification
[Success criteria and how to check — see D7 below]

## Resources
[Links to references/ — see D9 below]
```

#### 4c. Write Workflows (D4: Step Decomposition)

Research (CoM, ACL 2025; Watch Every Step, EMNLP 2024) proves numbered steps with decision points outperform free-form descriptions.

```markdown
# BAD — paragraph description
Process the document by extracting key fields and validating them
against the schema, then generating a report.

# GOOD — numbered steps with branching
## Workflow

1. **Extract**: Read document, extract fields in `references/schema.md`
2. **Validate**: Check each field against schema rules
   - If valid → proceed to step 3
   - If invalid → report specific errors, suggest fixes, STOP
3. **Transform**: Run `scripts/transform.py --input <extracted.json>`
4. **Report**: Generate output using `assets/report-template.md`
5. **Verify**: Confirm output contains all required sections
```

#### 4d. Write Constraints (D5: Positive Framing)

Inverse IFEval (ByteDance, 2025, 1012 test cases) proves positive constraints are followed significantly more reliably. Constraint Decomposition (2025): 41.2% → 73.8% accuracy when constraints are decomposed.

```markdown
# BAD — negative constraints
Don't write functions longer than 20 lines.
Never modify files outside the project.
Avoid using deprecated APIs.

# GOOD — positive constraints with specifics
Keep every function under 20 lines. Extract helpers for complex logic.
Only modify files within the target directory specified by the user.
Use APIs from the approved list in `references/api-versions.md`.
```

For safety-critical rules, keep negative framing but pair with positive alternative:
```markdown
CRITICAL: Only delete files after explicit user confirmation. (safety negative)
Prefer creating new files over modifying existing ones when possible. (positive alternative)
```

#### 4e. Write Examples (D6: Example Design)

Cursor official data: Good/Bad examples make rules **~3x more effective**. ACL 2025: 1-shot achieves best flexibility/structure balance.

```markdown
# BAD — abstract
Use the transform script to convert between formats.

# GOOD — concrete "user request → agent behavior"
## Examples

### User: "Convert this CSV to JSON"
→ 1. Run `scripts/transform.py data.csv --output data.json`
→ 2. Verify JSON has keys: `name`, `date`, `amount`
→ 3. Report: "Converted 150 records from CSV to JSON"

### User: "The output has wrong date format"
→ 1. Check current date format in output
→ 2. Add `--date-format ISO8601` flag
→ 3. Re-run and verify dates match `YYYY-MM-DD`
```

Include 1-3 examples in SKILL.md. For more, create `references/examples.md`.

#### 4f. Write Verification (D7: Verification)

Issue #42796 (1781👍): Analysis of 6,852 sessions shows agent Read:Edit ratio dropped 70%, causing "rush to completion" errors. Explicit verification steps prevent this.

```markdown
## Verification

After completing the workflow:
1. **Output exists**: Confirm the output file was created
2. **Schema valid**: Run `scripts/validate.py output.json`
3. **Content complete**: Output has all required sections
4. **No regressions**: Run `npm test`

If any check fails → diagnose, fix, re-verify.
```

#### 4g. Calibrate Freedom (D8: Freedom Calibration)

Match specificity to task fragility (NeurIPS 2024: task type determines optimal approach):

| Task Fragility | Freedom Level | How to Write |
|---|---|---|
| **Fragile** (deployment, DB migration, security) | Low — specific scripts + numbered steps | "Run `scripts/backup.sh` then `scripts/migrate.py --dry-run`" |
| **Moderate** (API calls, code generation) | Medium — preferred patterns + alternatives | "Prefer pdfplumber. For encrypted PDFs, use PyMuPDF instead." |
| **Open** (writing, brainstorming, design) | High — principles + examples | "Match brand voice in `references/brand-voice.md`. Target 500-800 words." |

#### 4h. Manage Context (D2 + D9: Efficiency + Progressive Loading)

**D2 — Token economy:** Every line must earn its cost. Delete what the model already knows. One example beats three paragraphs.

**D9 — Progressive loading:** Keep SKILL.md < 500 lines. Move details to `references/` with explicit "when to read" pointers:

```markdown
## Resources

- **Advanced schemas**: See [SCHEMAS.md](references/schemas.md) when user provides non-standard input
- **Error handling**: See [TROUBLESHOOTING.md](references/troubleshooting.md) when scripts fail
- **API reference**: See [API.md](references/api.md) when working with specific endpoints
```

Keep references one level deep (no nested references). Files > 100 lines: include table of contents at top.

### Step 5: Package

```bash
scripts/package_skill.py <path/to/skill-folder> [output-dir]
```

Automatically validates structure, frontmatter, naming, and description quality before packaging.

### Step 6: Iterate

1. Use the skill on real tasks
2. Notice struggles or inefficiencies
3. Apply Step 7 (Optimize) to systematically improve

---

## OPTIMIZE Mode: Step 7

Use when an existing skill needs improvement. Read `references/skill-optimization.md` for detailed before/after examples and `references/evidence-database.md` for research sources.

### 7.1 Diagnose

Read the full skill. Answer each diagnostic question:

| ID | Dimension | Diagnostic Question | Impact if Failing |
|---|-----------|-------------------|---|
| D1 | **Description** | Seeing ONLY name+description, would an AI trigger this skill correctly? | Skill never triggers or triggers incorrectly |
| D2 | **Efficiency** | Does every line earn its token cost? | Context bloat degrades all loaded skills |
| D3 | **Structure** | Are workflows/constraints/examples visually separated? | Instructions blur together, compliance drops |
| D4 | **Steps** | Are complex processes numbered with decision points? | Agent improvises, misses critical sequence |
| D5 | **Positive** | Are rules "do X" not "don't do Y"? | Negative constraints poorly followed (IFEval data) |
| D6 | **Examples** | Is there a concrete "user request → behavior" example? | Agent guesses expected behavior |
| D7 | **Verification** | Does the skill define how to check output? | Agent "rushes to completion" (Issue #42796) |
| D8 | **Freedom** | Is specificity matched to task fragility? | Over/under-constrained output |
| D9 | **Progressive** | Is SKILL.md lean with details in references/? | All content loaded even when not needed |

Run `scripts/quick_validate.py <skill-path>` for automated hints on D1, D2, D5, D6, D7, D9.

### 7.2 Prioritize by Skill Type

Focus on the dimensions that matter most for this skill type:

| Skill Type | Fix These First | Why |
|---|---|---|
| **Workflow** (sequential process) | D4 Steps → D7 Verify → D2 Efficiency | Sequence errors are catastrophic; verification catches them |
| **Tool Integration** (API/CLI wrapper) | D1 Description → D8 Freedom → D6 Examples | Must trigger on right tool names; right specificity level |
| **Knowledge/Reference** (schemas, policies) | D9 Progressive → D2 Efficiency → D3 Structure | Massive content needs aggressive context management |
| **Creative/Generative** (writing, design) | D5 Positive → D8 Freedom → D6 Examples | Needs principles not rigid rules; examples set quality bar |
| **Debugging/Analysis** (troubleshooting) | D4 Steps → D7 Verify → D5 Positive | Must follow diagnostic sequence; verify fix actually works |
| **Document Generation** (reports, analysis) | D4 Steps → D3 Structure → D7 Verify | Output structure must be fixed; verification ensures completeness |
| **Orchestration** (multi-agent, parallel tasks) | D4 Steps → D7 Verify → D6 Examples | Dispatch logic must be precise; sub-agent prompts need templates |
| **Meta-Skill** (skills about skills) | D3 Structure → D9 Progressive → D5 Positive | Complex logic needs clean structure; must avoid recursive bloat |
| **Quality Assurance** (review, testing, verification) | D7 Verify → D5 Positive → D4 Steps | Verification is the core function; positive framing prevents over-flagging |

### 7.3 Apply Dimension Fixes

For each failing dimension, apply the fix. See `references/skill-optimization.md` for detailed before/after examples.

**D1 — Rewrite description** with 3-part formula: (1) capabilities, (2) trigger scenarios, (3) keywords.

**D2 — Audit every line**: delete known knowledge, compress with examples, move details to `references/`. Target < 500 lines.

**D3 — Add visual hierarchy**: Markdown `##`/`###` headings for each content type. `---` between major blocks.

**D4 — Number the steps**: Convert paragraphs to numbered lists. Add `if/else` decision points. Add error handling.

**D5 — Flip to positive**: Convert "don't X" → "do Y". For safety rules, keep negative but add positive alternative.

**D6 — Add examples**: 1-3 concrete "User: ... → Agent behavior: ..." examples. Realistic inputs, not placeholders.

**D7 — Add verification**: Explicit success criteria at workflow end. What to check, how to check, what if it fails.

**D8 — Calibrate freedom**: Fragile tasks → numbered steps/scripts. Creative tasks → principles/examples.

**D9 — Move to references**: Anything beyond core workflow → `references/`. Each link says WHEN to read it.

### 7.4 Scan for Anti-Patterns

| Anti-Pattern | Symptom | Fix |
|---|---|---|
| **Kitchen Sink** | SKILL.md > 500 lines | Split into focused skills or references/ |
| **Invisible Skill** | No trigger phrases in description | Rewrite with Trigger: keywords |
| **Vague Guardrails** | "Write clean code", "Be helpful" | Replace with specific, measurable rules |
| **Negative-Only** | Mostly "don't" / "never" rules | Convert to positive framing |
| **Missing Exit** | No success/failure criteria | Add verification section |
| **Flat Wall of Text** | No headings or visual breaks | Add ## / ### headings |
| **Zombie References** | Files exist but unlinked from SKILL.md | Add explicit "See X when Y" pointers |
| **Example-Free** | No concrete examples | Add 1-3 user request → behavior examples |
| **Stateless Multi-Step** | Multi-step workflow with no state tracking | Add file existence checks or checkbox tracking |
| **LLM-as-State-Oracle** | Using LLM to determine workflow state instead of scripts | Replace with deterministic checks (file exists, script output) |
| **Missing Script Integration** | References to scripts/ but no scripts/ directory | Create the scripts or remove references |

### 7.5 Validate After Optimization

1. Run `scripts/quick_validate.py <skill-path>` — structure + optimization hints
2. Re-read end-to-end — does each section serve a clear purpose?
3. Count lines — SKILL.md body still < 500?
4. Check all reference links — valid? Explain when to read?

---

## Reference Files

| File | When to Read |
|---|---|
| `references/skill-optimization.md` | Optimizing a skill — detailed before/after examples for all 9 dimensions |
| `references/evidence-database.md` | Checking research evidence — papers, data, community issues |
| `references/skill-taxonomy.md` | Classifying skill types — 9 types, design templates, user need routing |
| `references/state-machine-patterns.md` | Adding state management — DAG patterns, checkpoint design, script-driven workflows |

## Scripts

| Script | Purpose |
|---|---|
| `scripts/init_skill.py` | Create new skill directory with optimized template |
| `scripts/package_skill.py` | Validate + package skill into .skill file |
| `scripts/quick_validate.py` | Validate structure + check optimization hints |
