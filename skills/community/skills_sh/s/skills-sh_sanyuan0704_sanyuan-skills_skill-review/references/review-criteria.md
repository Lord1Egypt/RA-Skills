# Review Criteria Reference

Detailed criteria for each review dimension. Load this file during Step 2 analysis.

## Structure Compliance — Detailed Checks

### Required
- `SKILL.md` exists at root
- Frontmatter has `name` field (matches directory name)
- Frontmatter has `description` field (non-empty, >50 chars)

### Expected
- `SKILL.md` ≤ 500 lines (hard limit; flag if >400 as approaching)
- No files that serve no purpose: README.md (unless skill IS about READMEs), CHANGELOG.md, CONTRIBUTING.md
- `scripts/` — if present, all files are executable and tested
- `references/` — if present, each file is referenced from SKILL.md with load instructions
- `assets/` — if present, files are used in output, not loaded into context

### Red Flags
- SKILL.md > 500 lines → must extract to references
- Deeply nested references (2+ levels) → flatten
- Orphaned files (not referenced from SKILL.md)
- Scripts without clear invocation instructions in SKILL.md

## Description Quality — Detailed Checks

### Keyword Bombing Indicators (Good)
- 3+ verb variations for the same action (create/build/write/make)
- Noun variations (skill/agent/tool/plugin)
- Natural phrases a user would type
- Both imperative ("create a skill") and question form ("how do I build a skill")

### Description Anti-Patterns (Bad)
- Single-sentence description under 100 characters
- Only technical terms, no natural language triggers
- Describes implementation ("Uses markdown frontmatter...") instead of user intent
- Contains instructions meant for the model body

### Scoring Heuristic
- Count unique trigger phrases → <3 is weak, 5-8 is good, >10 is excellent
- Check if casual user language would match → try 3 hypothetical queries mentally

## Workflow Design — Detailed Checks

### Checklist Quality
- Uses `- [ ]` format (copy-paste friendly)
- Steps are numbered and sequential
- Sub-steps use indentation
- ⚠️ marks appear on steps that must not be skipped
- ⛔ marks appear on prerequisites/blockers

### Confirmation Gates
Must exist before:
- File creation/deletion/overwrite
- External API calls with side effects
- Long-running generative operations
- Applying analysis results to code

### Flow Quality
- Can a reader understand the full process from the checklist alone?
- Are conditional branches clearly marked?
- Is there a clear start and end state?

## Token Efficiency — Detailed Checks

### Iron Law
- Present: yes/no
- Placed at top (before workflow): yes/no
- Specific and falsifiable: yes/no (bad: "write good code"; good: "never use placeholder text")
- Addresses the #1 likely failure mode: yes/no

### Progressive Loading Signals (Good)
- "Load references/X.md for..." with clear trigger conditions
- References loaded at specific workflow steps, not all in Step 1
- Large context only loaded when that branch is taken

### Bloat Signals (Bad)
- Explaining things Claude knows (how to write markdown, what JSON is)
- "You should" / "You will" / "Remember to" (wasted tokens on filler)
- Duplicated instructions (same thing said in workflow AND in later section)
- Comments/explanations aimed at human readers, not model behavior

## Anti-Pattern Detection — Detailed Examples

### Vague Directives (rewrite as questions)
- ❌ "Ensure the output is high quality"
- ✅ "Does every heading have ≥2 sentences of content beneath it?"

### Over-Specification
- ❌ "Use markdown headers with # for h1, ## for h2..." (Claude knows this)
- ✅ "Use exactly 2 levels of headers: # for sections, ## for subsections" (this constrains)

### Missing Guardrails
- No anti-patterns section = model will take lazy defaults
- No pre-delivery checklist = no verification step
- No Iron Law = no north star for quality decisions

### Monolithic SKILL.md
- If SKILL.md > 300 lines, check: could any section be a reference loaded on-demand?
- Domain knowledge that applies to only one step → extract to reference
- Examples longer than 10 lines → extract to reference
