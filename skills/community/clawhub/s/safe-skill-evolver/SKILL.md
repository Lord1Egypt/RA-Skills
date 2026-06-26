# Skill Evolver

**A safe, diff-based skill builder and optimizer for OpenClaw.**

**NEVER applies changes automatically. Always suggests diffs and waits for explicit user confirmation.**

---

## When to Use

Use this skill when the user wants to:

1. **Create a new skill** — from scratch or based on an existing template
2. **Improve an existing skill** — analyze errors, feedback, or usage patterns and suggest enhancements
3. **Audit/review a skill** — check quality, security, completeness of any SKILL.md
4. **Migrate or refactor** — restructure skills between workspaces, vaults, or formats

---

## Core Principles

### Safety First
- **NEVER write files without explicit user confirmation.**
- **ALWAYS present a diff/preview before applying changes.**
- **NEVER execute shell commands from skill logic.**
- Skills can read anything; they can only write what the user explicitly approves.

### Transparent Process
Every operation follows this workflow:

```
ANALYZE → SUGGEST → REVIEW → CONFIRM → APPLY
```

- **Analyze:** Read existing files, understand context, identify gaps or issues.
- **Suggest:** Generate proposed changes as a clear diff or structured preview.
- **Review:** Explain *why* each change is recommended (rationale).
- **Confirm:** Wait for explicit user approval ("ja", "ok", "apply", "bestätigen").
- **Apply:** Only then write files, create directories, or modify skills.

---

## Skill Anatomy

A valid OpenClaw skill requires:

| Component | Required | Description |
|-----------|----------|-------------|
| `SKILL.md` | ✅ Yes | Core definition: triggers, workflow, safety rules, examples |
| `scripts/` | ⚪ Optional | Helper scripts (Python, PowerShell, JS) |
| `templates/` | ⚪ Optional | Reusable templates for generating new skills |
| `references/` | ⚪ Optional | External docs, patterns, examples referenced by SKILL.md |
| `README.md` | ⚪ Optional | Human-friendly overview for ClawHub publishing |
| `LICENSE` | ⚪ Optional | License file for distribution |

### SKILL.md Structure

```markdown
# Skill Name

## When to Use
[Clear trigger conditions]

## Core Principles
[Safety rules, boundaries]

## Workflow
[Step-by-step process]

## Tools / Scripts
[Reference to helper scripts]

## Examples
[Concrete usage examples]

## Safety & Boundaries
[What NOT to do]
```

---

## Workflows

### 1. Create New Skill (Builder Mode)

**Trigger:** User says "create skill for X", "build a skill that does Y", "new SKILL.md for Z"

**Steps:**

1. **Gather Requirements**
   - What problem does the skill solve?
   - What triggers should activate it?
   - What tools/commands does it need?
   - What are the safety boundaries?

2. **Select or Design Template**
   - For simple skills: use `templates/basic_skill.md`
   - For tool-heavy skills: use `templates/tool_skill.md`
   - For complex workflows: use `templates/workflow_skill.md`

3. **Generate Draft**
   - Fill template with gathered requirements
   - Ensure all required sections are present
   - Add concrete examples

4. **Present Diff**
   - Show the complete proposed SKILL.md
   - Highlight: triggers, safety rules, boundaries
   - Ask for confirmation

5. **Apply on Confirm**
   - Create directory: `<skill-name>/`
   - Write `SKILL.md`
   - Create subdirectories (`scripts/`, `templates/`) if needed
   - Report success and next steps

---

### 2. Improve Existing Skill (Evolver Mode)

**Trigger:** User says "improve skill X", "optimize this skill", "skill Y has errors", "evolve skill Z"

**Steps:**

1. **Analyze Current State**
   - Read the existing `SKILL.md`
   - Check for: completeness, clarity, safety gaps, outdated info
   - If error reports exist, read `ERRORS.md` or session logs
   - Identify what's working and what's not

2. **Identify Improvement Opportunities**

   | Category | What to Check |
   |----------|---------------|
   | **Triggers** | Are trigger conditions clear and complete? |
   | **Workflow** | Is the step-by-step process logical and safe? |
   | **Safety** | Are boundaries explicit? Is auto-write prevented? |
   | **Examples** | Are there concrete, realistic usage examples? |
   | **Tools** | Are referenced scripts still valid and secure? |
   | **Format** | Follows OpenClaw SKILL.md conventions? |

3. **Generate Diff**
   - Present changes as `before → after` blocks
   - Group by category (triggers, workflow, safety, examples)
   - Explain rationale for each change

4. **Review with User**
   - Summarize: "I suggest 5 changes: 2 safety improvements, 1 new trigger, 2 clarified examples"
   - Show full diff
   - Ask: "Soll ich diese Änderungen übernehmen?"

5. **Apply on Confirm**
   - Update `SKILL.md` (backup old version)
   - Update related scripts/templates if affected
   - Report what changed and why

---

### 3. Audit / Review Mode

**Trigger:** User says "review this skill", "audit skill X", "is this skill safe?"

**Steps:**

1. Read the complete skill directory
2. Check against quality checklist (see below)
3. Output structured report with:
   - ✅ Strengths
   - ⚠️ Gaps / Risks
   - 💡 Improvement suggestions
4. **Do NOT modify anything** — this is read-only

---

## Quality Checklist

When auditing or improving a skill, verify:

### Completeness
- [ ] `SKILL.md` exists and is non-empty
- [ ] "When to Use" section is clear and specific
- [ ] At least one concrete usage example
- [ ] All referenced scripts/templates exist

### Safety
- [ ] Explicit "never auto-execute" rule present
- [ ] External actions (write, exec) require confirmation
- [ ] No hardcoded secrets or credentials
- [ ] Boundary conditions documented (what NOT to do)

### Clarity
- [ ] Trigger conditions are unambiguous
- [ ] Workflow steps are numbered or clearly sequenced
- [ ] Technical terms are explained or linked
- [ ] Examples cover success AND error cases

### Maintainability
- [ ] Version/tag noted
- [ ] Last updated date present
- [ ] Changelog if skill evolved
- [ ] Dependencies documented

---

## Templates

Use the templates in `templates/` directory:

- **`basic_skill.md`** — Simple knowledge/pattern skill (no scripts)
- **`tool_skill.md`** — Skill wrapping scripts or external tools
- **`workflow_skill.md`** — Multi-step process skill with decision trees
- **`evolver_task.md`** — Task template for recording improvement opportunities

---

## Scripts

### `scripts/analyze_skill.py`
Reads a SKILL.md and returns structured analysis:
- Word count, section completeness
- Trigger clarity score
- Safety rule presence
- Example count

### `scripts/generate_diff.py`
Compares two SKILL.md versions and outputs a human-readable diff.

### `scripts/validate_skill.py`
Checks a skill directory against the Quality Checklist above.

---

## Safety & Boundaries

### NEVER
- Write or modify any file without explicit user confirmation
- Confirm before write: Always ask user before writing files
- Confirm before execute: Always ask user before running commands
- Execute shell commands from skill logic without approval
- Auto-publish skills to ClawHub without review
- Delete existing skills without backup
- Ignore safety warnings during audit

### ALWAYS
- Present a clear diff before applying changes
- Explain WHY each change is suggested
- Backup the old version before overwriting
- Respect user rejection — if they say "nein", stop immediately
- Log what was changed in `LEARNINGS.md` or session notes

### WHEN IN DOUBT
- Ask the user before proceeding
- Prefer read-only analysis over automatic modification
- Document uncertainty in the suggestion rationale

---

## Examples

### Example 1: Create New Skill

**User:** *"Ich brauch einen Skill für GPU-Transkription mit faster-whisper"*

**Skill Evolver:**
1. Gathers requirements: Audio file path, model size, language
2. Selects `tool_skill.md` template
3. Generates draft with:
   - Triggers: User mentions "transcribe", "whisper", "audio to text"
   - Workflow: Validate path → Check GPU → Run faster-whisper → Return text
   - Safety: Never auto-delete audio files, validate paths before reading
4. Presents complete SKILL.md
5. **Waits for confirmation:** *"Soll ich diesen Skill als `gpu-transcribe` anlegen?"*
6. On "ja": Creates `gpu-transcribe/SKILL.md` and reports success

### Example 2: Improve Existing Skill

**User:** *"Der paperclip-skill startet manchmal Embedded-Postgres, obwohl externe DB konfiguriert ist"*

**Skill Evolver:**
1. Reads existing paperclip SKILL.md
2. Analyzes: Missing environment variable check in startup workflow
3. Identifies gap: No validation of `DATABASE_URL` before fallback to embedded
4. Generates diff:
   - **Before:** "Start paperclip → if no DB, use embedded"
   - **After:** "Check DATABASE_URL env var → if set, validate connection → only if unset/missing, warn user and abort (never auto-start embedded)"
5. **Presents diff with rationale**
6. On confirmation: Updates SKILL.md, backs up old version

### Example 3: Audit Skill for Safety

**User:** *"Kannst du den evolver-skill von ClawHub auditen?"*

**Skill Evolver:**
1. Reads the skill's files (SKILL.md, scripts, etc.)
2. Checks against Quality Checklist
3. Outputs report:
   - ✅ Good: Clear triggers, structured workflow
   - ⚠️ Risk: Script references external URLs without validation
   - ⚠️ Risk: No explicit "ask before write" boundary
   - 💡 Suggest: Add URL whitelist, add confirmation rule
4. **Does NOT modify anything** — read-only audit

---

## Metadata

- **Version:** 1.0.0
- **Created:** 2026-05-28
- **Updated:** 2026-05-28
- **Author:** OpenClaw (for Andreas)
- **License:** MIT-0
- **Tags:** skill-builder, skill-optimizer, diff-based, safe, workflow
