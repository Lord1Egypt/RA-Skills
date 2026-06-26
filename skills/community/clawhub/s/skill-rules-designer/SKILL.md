---
name: skill-rules-designer
version: v1.2
description: >
  Analyzes an existing Claude Code skill and designs an optimal rules/ file structure.
  Covers three operations: (1) compressing SKILL.md by moving verbose content into rules modules,
  (2) encapsulating optional features so they only load when needed — reducing per-invocation token
  cost, (3) enriching the skill with new template or resource files for steps that currently require
  the model to reinvent from scratch each time. Also identifies vague instructions and rewrites them
  to be precise. All operations are lossless — original content is always preserved or explicitly
  moved, never deleted without a destination.
  Use this skill whenever someone says "my skill is too long", "help me structure my rules files",
  "split this skill", "reduce token usage", "add a template to my skill", "make this rule more
  precise", or shows you a SKILL.md and asks how to improve its structure or efficiency.
---

# Skill Rules Designer

You help users restructure existing Claude Code skills. The guiding principle is **lossless
restructuring**: every operation either moves content to a new location, or adds new content.
Nothing is ever deleted without being placed somewhere else first.

There are four things you can do to a skill, and you should analyze which apply:

1. **Compress** — move verbose content from SKILL.md into a rules file. SKILL.md gets shorter,
   total content is unchanged, per-invocation token cost is unchanged (rules files in a skill's
   directory are still loaded). Worth doing for readability and maintainability.

2. **Encapsulate** — move content that is only needed in some invocations into a rules file that
   is loaded conditionally. SKILL.md shrinks AND per-invocation token cost drops. This is the
   highest-value operation.

3. **Enrich** — create a new rules file containing templates, checklists, or scripts for something
   the skill currently handles by ad-hoc reasoning each time. Doesn't shorten SKILL.md but makes
   the skill faster, more consistent, and more capable.

4. **Harden** — rewrite vague instructions in any file to make them precise and unambiguous. No
   structural change; improves reliability.

Always show a plan first. Wait for user confirmation before writing anything.

---

## Step 1: Read the skill

Ask for the skill directory path (or accept it if already provided).

Read:
- `SKILL.md` (required — stop if missing)
- All existing `rules/*.md` files
- Any `scripts/` or `assets/` directories (note what exists)

Build a mental model: what does this skill do, what are its phases, what files exist?

Print a one-line inventory:
```
skill-track — SKILL.md (59 lines) + 6 rules files (640 lines total)
```

---

## Step 2: Analyze each dimension

Work through each of the four operations. For each one, identify specific candidates.

### Compress candidates
Look for content in SKILL.md that is:
- Detailed reference material (tables, schemas, long examples)
- A complete self-contained phase that could be a standalone document
- More than ~30 lines that are unlikely to change what the model does if removed from direct view

For each candidate: name it, estimate line count, state what file it would move to.

### Encapsulate candidates
Look for content in SKILL.md (or existing rules files) that is only needed sometimes:
- Features gated by a user choice (e.g., "only if the user asks for PDF export")
- Error handling paths that rarely trigger
- A whole workflow branch that applies to one mode but not another

For each candidate: name it, estimate token savings per typical invocation, state the condition
that gates it.

### Enrich candidates
Look for steps where the skill currently says something like:
- "generate a report" without a template
- "format the output" without a format spec
- "commit with a conventional message" without examples
- Any multi-step procedure that a user would want to be consistent across runs

For each candidate: describe what the new file would contain, why it saves the model from
reasoning from scratch, and what the skill currently does instead.

### Harden candidates
Look for instructions that use vague verbs or implicit branching:
- "handle X appropriately", "process as needed", "if relevant"
- A check or guard rail with no consequence defined for failure
- A decision (if A then B) where the else case is missing

For each candidate: quote the original, explain the ambiguity, propose a precise rewrite.

---

## Step 3: Present the plan

Use this format:

```
## Restructuring Plan — [skill name]

Current: SKILL.md ([N] lines) + [N] rules files
After:   SKILL.md (~[N] lines) + [N] rules files

### Compress
→ Move [section name] (~[N] lines) → rules/[filename].md
  [One sentence on why this is worth doing]

→ (or: Nothing to compress — SKILL.md is already lean)

### Encapsulate
→ Move [section name] (~[N] lines) → rules/[filename].md
  Condition: only loaded when [specific trigger]
  Token savings: ~[N] lines on typical invocations that skip this path

→ (or: No clear encapsulation opportunities)

### Enrich
→ New file: rules/[filename].md
  Contains: [what it holds — template, checklist, script]
  Replaces: [what the skill currently does ad-hoc]

→ (or: No enrichment needed)

### Harden
1. [file:line] "[original quote]"
   Problem: [why it's ambiguous]
   Proposed: "[precise rewrite]"

→ (or: No vague instructions found)

---
Lossless check: all content currently in SKILL.md will exist in the new file set.
No original content is removed without a destination.
```

After the plan, ask:

```
Does this look right? Tell me:
- Any changes to the plan
- Which operations to skip
- Whether to write all files at once or one at a time

Say "go" to proceed.
```

---

## Step 4: Write the files

Once confirmed, write in this order to preserve losslessness:

1. Create new `rules/*.md` files with the content they'll receive
2. Update SKILL.md — remove only the content that was written in step 1
3. If enriching: create new template/resource files

Never remove content from SKILL.md until it has been written to its destination file.

Each new rules file structure:
```markdown
# [filename] — [one-line purpose]

[Content]
```

References in updated SKILL.md:
```markdown
## Modules
- `rules/[name].md` — [when to read it]
```

Print a summary when done:
```
Done.
  ✓ Created rules/[name].md ([N] lines)  [compress/encapsulate/enrich]
  ✓ Updated SKILL.md: [before] → [after] lines

Token impact: [N] lines removed from always-loaded context.
[Module] only loads when [condition] — saves ~[N] tokens on [typical scenario].
```

---

## Losslessness rules

The restructuring is lossless when:
- Every line removed from SKILL.md appears verbatim (or explicitly rewritten) in a rules file
- No rules file is created without a corresponding reference added to SKILL.md
- Hardening rewrites preserve the original intent — they clarify, not change, behavior
- If the user later removes all rules files, SKILL.md still describes the skill's full scope
  (even if the detail lives elsewhere)

If the user asks you to delete a section with no destination, propose a destination first.
If no destination makes sense, suggest keeping it in SKILL.md even if it's long.

---

## Evaluating the skill (A/B comparison)

Use this when the user wants to compare two versions of a skill (e.g., before and after a
restructuring) to check whether quality degraded and quantify the token/time tradeoff.

This section follows the same pattern as skill-creator's eval workflow. Read the agent files
in `agents/` and the schemas in `references/schemas.md` when running evals.

### Step 1: Set up the workspace

```
<skill-name>-workspace/
  ab-comparison/
    eval-1/
      version_a/outputs/
      version_b/outputs/
    eval-2/
      version_a/outputs/
      version_b/outputs/
    eval-3/
      version_a/outputs/
      version_b/outputs/
```

Create an `eval_metadata.json` in each eval directory:

```json
{
  "eval_id": 1,
  "eval_name": "descriptive-name-here",
  "prompt": "The eval prompt",
  "assertions": []
}
```

### Step 2: Spawn all runs in the same turn

For each of the 3 test cases (see `evals/evals.json`), spawn two subagents simultaneously:
- **version_a**: the original (or current) skill
- **version_b**: the restructured (or candidate) skill

Prompt template for each executor subagent:

```
Execute this task using the skill at <skill-path>:

Task: <eval prompt>
Save all output files to: <workspace>/ab-comparison/eval-<ID>/<version>/outputs/
Also save a transcript.md summarizing your steps to that same outputs/ directory.
```

While runs execute, draft assertions for each eval and add them to `eval_metadata.json`.

Good assertions for skill-rules-designer check:
- Whether a plan was presented before files were written
- Whether at least one rules/*.md file was created (for compress/encapsulate/enrich evals)
- Whether SKILL.md was updated with references after content was moved
- Whether the losslessness guarantee holds (content removed from SKILL.md exists in destination)
- Whether the before/after line count summary was printed

### Step 3: Capture timing

When each subagent completes, save the `total_tokens` and `duration_ms` from the task
notification immediately to `timing.json` in the run directory. This data is not persisted
elsewhere.

### Step 4: Grade each run

Spawn a grader subagent per run using `agents/grader.md`. Save results to `grading.json`
in each run directory (sibling to `outputs/`).

### Step 5: Build benchmark.json

Create `benchmark.json` at the workspace root using the schema in `references/schemas.md`.
Use `"version_a"` and `"version_b"` as the `configuration` values. Include:
- Individual run results with pass_rate, tokens, time_seconds
- `run_summary` with mean ± stddev for both versions and the `delta`
- `notes` from an analyst pass (read `agents/analyzer.md` — "Analyzing Benchmark Results" section)

### Step 6: Print the comparison report

Print a formatted summary directly in the terminal. No viewer needed.

```
## A/B Comparison — skill-rules-designer
─────────────────────────────────────────────────

  Quality (Pass Rate)   Version A: 86%   Version B: 71%   Δ +15%  ✓ A wins
  Token Usage           Version A: 42,500  Version B: 31,000  Δ +37%  ✗ A costs more
  Duration              Version A: 95s   Version B: 78s   Δ +22%  ✗ A is slower

─────────────────────────────────────────────────
Per-eval breakdown:

  Eval 1 — compress-and-encapsulate
    Version A: 6/7 passed (86%)  │ 95s │ 42,500 tok
    Version B: 5/7 passed (71%)  │ 80s │ 32,000 tok
    ✗ Version B missed: "SKILL.md updated with module references"

  Eval 2 — harden-vague-instructions
    Version A: 7/7 passed (100%) │ 88s │ 39,000 tok
    Version B: 4/7 passed (57%)  │ 72s │ 28,000 tok
    ✗ Version B missed: "Quotes the original instruction verbatim"
                        "Explains the ambiguity precisely"
                        "Presents change as plan before applying"

  Eval 3 — enrich-with-template
    Version A: 6/7 passed (86%)  │ 102s │ 46,500 tok
    Version B: 6/7 passed (86%)  │ 82s │ 33,000 tok
    ✗ Both missed: "Template contains actual section headers"

─────────────────────────────────────────────────
Analysis notes:
  • Version A consistently enforces plan-before-write; Version B skips it under time pressure
  • Token cost of Version A is higher due to additional losslessness verification steps
  • Eval 2 shows the largest quality gap — harden workflow needs clearer trigger in Version B
```

Adapt the actual numbers and missed assertions from the real grading results.

### Step 7: Optional blind comparison

For deeper analysis, run the blind comparator on each eval's outputs:

1. Give both outputs to a subagent using `agents/comparator.md` without revealing which is A/B
2. Save results to `comparison-<eval_id>.json`
3. Run post-hoc analysis using `agents/analyzer.md` to understand why the winner won

See `references/schemas.md` for the `comparison.json` and `analysis.json` schemas.

---

## Reference files

- `agents/grader.md` — How to evaluate assertions against outputs
- `agents/comparator.md` — How to do blind A/B comparison between two outputs
- `agents/analyzer.md` — How to analyze why one version beat another
- `references/schemas.md` — JSON schemas for evals.json, grading.json, benchmark.json, etc.
- `evals/evals.json` — The 3 test cases for this skill
