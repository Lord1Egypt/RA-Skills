---
name: skill-optimizer
description: Audit and improve existing Agent Skills (SKILL.md files) against the agentskills.io standard. Use this skill whenever the user wants to optimize, polish, improve, audit, review, fix, or refine an existing skill — even if they don't say "skill optimizer" explicitly. Triggers on phrases like "improve my skill", "audit SKILL.md", "make my skill trigger better", "fix the description", "is my skill well written?", "review this skill", "polish my skill", "this skill underperforms", or any request to update a SKILL.md for clarity, triggering accuracy, or structure. Runs a 3-dimension audit (Specification / Best Practices / Description Optimization), produces a severity-ranked report, and proposes concrete edits. For full eval-driven iteration with baseline comparisons, defer to the skill-creator skill.
---

# Skill Optimizer

A focused, opinionated tool for auditing and improving **existing** Agent Skills. Where `skill-creator` covers the full create-from-scratch workflow (interview → draft → eval → iterate), this skill is the lighter, faster counterpart you reach for when the skill already exists and the question is "how do I make it better?"

The optimization framework is built directly on the three pillars from [agentskills.io](https://agentskills.io/):

1. **Specification** — Is the file structurally valid? Does the frontmatter conform? Are naming and length rules respected?
2. **Best Practices** — Is the content clear, scoped, and well-organized? Does it follow the writing patterns the agentskills.io guide recommends?
3. **Description Optimization** — Will the skill trigger on the right prompts and stay quiet on the wrong ones? Are the right keywords and intent signals present?

When the user wants full eval-driven iteration with subagent runs, baseline comparisons, and an HTML viewer, defer to the `skill-creator` skill. Use this skill for everything else.

---

## When to use

Use this skill for any of:

- "Audit my skill against the spec" / "is this SKILL.md well formed?"
- "Improve the triggering of my skill" / "my skill isn't firing on the right prompts"
- "Make the description better" / "rewrite the frontmatter description"
- "This skill is too long, help me trim it"
- "Review this skill before I publish it"
- "Add examples and gotchas to my skill"
- Any request to edit, polish, or refine an existing `SKILL.md`

Do not use this skill to **create** a new skill from scratch — for that, start with `skill-creator`. If the user has a draft and wants to run evals, hand off to `skill-creator` after the first pass here.

---

## The 3-dimension audit

Every optimization pass runs the same three dimensions. The order matters — fix Specification issues first, then Best Practices, then Description. A skill that violates the spec won't even load; a skill with bad content won't produce good outputs; a skill with a bad description won't be reached at all.

### Dimension 1: Specification compliance

The spec is binary — either the file is valid or it isn't. Read the agentskills.io Specification in detail at `references/specification-checklist.md`. The audit covers:

- **`SKILL.md` exists** at the skill root.
- **YAML frontmatter is present**, well-formed, and has the required `name` and `description` fields.
- **`name`** is kebab-case, 1–64 chars, no leading/trailing hyphens, no consecutive hyphens, matches the parent directory.
- **`description`** is 1–1024 chars, no angle brackets, non-empty.
- **`compatibility`** (if present) is 1–500 chars.
- **No unexpected frontmatter keys** — only `name`, `description`, `license`, `allowed-tools`, `metadata`, `compatibility`.
- **Body length** stays under ~500 lines (recommendation) so the full file fits comfortably when activated.
- **File references** are one level deep from `SKILL.md` — no `references/sub/deep/file.md` chains.

Run `scripts/audit_skill.py <path>` to perform the mechanical checks. It returns the same errors and warnings the agentskills.io validator would catch, plus a few content-level checks (line count, body structure).

### Dimension 2: Best practices alignment

Best practices are softer — a skill can be spec-valid and still be vague, over-long, or unscoped. Read the detailed audit at `references/best-practices-checklist.md`. The key axes:

- **Scope**: One coherent unit of work. If the skill covers two unrelated domains, flag it for splitting.
- **Specificity calibration**: Flexible instructions for flexible tasks, prescriptive instructions for fragile ones. Rigid ALWAYS/NEVER directives are a yellow flag — check whether the underlying reason is explained.
- **Default + escape hatch**: When multiple tools or approaches could work, the skill should pick a default and mention alternatives briefly, not present them as equal options.
- **Procedure over declaration**: Skills should teach the model *how to approach* a class of problems, not just produce a specific answer.
- **Gotchas section**: Non-obvious, environment-specific corrections the model would get wrong without help. This is often the highest-value content in a skill.
- **Output templates**: When the skill produces structured output, a template is more reliable than prose describing the format.
- **Progressive disclosure**: Long skills move reference material to `references/` with explicit triggers (e.g. "Read `references/<topic>.md` if the API returns a non-200 status").
- **Token budget**: Add what the agent lacks, omit what it knows. Cut any sentence that explains what an LLM already knows (e.g., what a PDF is).

For each axis, give a verdict: **Pass / Warning / Fail** with one sentence of evidence.

### Dimension 3: Description optimization

The `description` field is the entire triggering mechanism. The agentskills.io guide emphasizes that agents only consult skills for tasks requiring knowledge beyond what they can handle alone — so simple one-step requests may not trigger even a perfect description. The audit covers the *wording*; triggering accuracy in practice also depends on the user actually having non-trivial work to do.

Read the full guide at `references/description-guide.md`. The audit checks:

- **Imperative framing**: "Use this skill when..." not "This skill does..."
- **User intent over implementation**: Describes what the user is trying to achieve, not internal mechanics.
- **Pushy coverage**: Explicitly lists contexts where the skill applies, including cases where the user doesn't name the domain directly ("even if they don't say 'X' explicitly").
- **Concrete keywords**: Specific phrases the user would actually type — file types, domain names, action verbs. Avoid generic verbs like "handle", "process", "deal with".
- **Length**: Stays under 1024 chars. Long descriptions are usually a sign of trying to enumerate every possible trigger — better to generalize.
- **No angle brackets**: Spec rule, will fail validation.
- **No vague verbs**: "Helps with PDFs" → "Extracts text and tables from PDFs, fills forms, merges files. Use when working with PDF documents."

The output of this dimension is a list of specific edits to the description, often in before/after form.

---

## Workflow

A single optimization pass follows this sequence. Skip steps only if the user is explicit ("just fix the description").

### Step 1: Capture intent (always)

Ask the user one focused question if it's not obvious: **What problem are you trying to solve with this skill?** Common intents:

- "It doesn't trigger when it should" → focus on Dimension 3.
- "The output quality is inconsistent" → focus on Dimension 2.
- "I want to publish it / the spec linter is failing" → focus on Dimension 1.
- "All of the above" → run the full audit.

Don't ask more than one question at a time. The user's intent shapes which dimensions get the deepest treatment.

### Step 2: Locate and snapshot

- Find the target `SKILL.md`. The user usually points at it directly. If not, search common locations: `~/.claude/skills/`, `~/.agents/skills/`, project-local `.claude/skills/`, plugin caches.
- Read the file in full before judging it.
- Snapshot the original (e.g., copy to `<workspace>/original-SKILL.md`) so the user can diff the changes. Don't write back to a read-only path without copying first.

### Step 3: Run the audit

Read the relevant reference checklist for each dimension as you go. Use the bundled `scripts/audit_skill.py` for the mechanical (Dimension 1) checks — it produces a structured pass/fail list. For Dimensions 2 and 3, do them by reading and applying the checklist; LLMs are better judges of content quality than regex.

### Step 4: Generate the report

Use the template at `assets/report-template.md`. Fill in:

- **Findings** grouped by dimension, each with a severity (Blocker / Major / Minor / Nit) and a one-sentence evidence statement.
- **Proposed edits** as concrete before/after diffs.
- **Effort estimate**: trivial edit / refactor / rewrite.

The report is what the user reviews and approves. Don't apply changes silently.

### Step 5: Apply with approval

Walk through each proposed edit with the user. For each:

- Show the diff.
- Explain *why* the change improves the skill (e.g., "this adds the 'even if you don't say CSV' pattern that boosts trigger recall on near-miss queries").
- Wait for approval.

Apply all approved edits, then re-run `scripts/audit_skill.py` to confirm the result is still spec-valid.

### Step 6: Optional — hand off to skill-creator for eval

If the user wants to verify the improvements actually change behavior (not just structure), hand off to `skill-creator`. That skill's eval-driven iteration is the right tool for measuring output quality, not this one. This skill optimizes the *artifact*; skill-creator measures the *outcome*.

---

## Outputs the user should expect

A single optimization pass produces:

1. A **report** (markdown, structured by dimension) with severity-ranked findings.
2. A set of **proposed edits** as diffs.
3. After approval, an **updated `SKILL.md`** plus a **validation pass** confirming the file is still spec-valid.

It does not produce: eval runs, baseline comparisons, triggering-rate measurements. Those are skill-creator's job.

---

## Common anti-patterns to flag

These come up over and over. When you see them, name them explicitly — the user is more likely to act on a named pattern than a generic "this is unclear."

- **Vague verb syndrome**: "Helps with X", "Processes X", "Manages X". Replace with the specific operations the skill performs.
- **Generic best-practices skill**: A skill that says "follow best practices for X" without any of *your* project's specifics. The agentskills.io guide is explicit: skills grounded in real expertise outperform ones synthesized from generic references. If a skill could apply to any project, it's probably not pulling its weight.
- **Kitchen-sink skill**: One skill that covers three domains. Flag for splitting — multiple narrow skills beat one broad one.
- **Tutorial instead of skill**: The body explains what a concept is (what a PDF is, how HTTP works) instead of focusing on what the model wouldn't know. Cut the background.
- **Bait description**: A description that lists every conceivable trigger keyword in a comma-separated list, hoping to match anything. This is overfitting — generalize to categories instead.
- **Missing gotchas**: A skill that doesn't list the non-obvious things the model would get wrong. The gotchas section is often the highest-leverage content.
- **No examples**: Output formats and edge cases are easier to convey with concrete examples than with prose.
- **Body longer than 500 lines**: Push detailed reference material to `references/` and tell the model *when* to read each file.

For the full list and how to fix each, see `references/common-issues.md`.

---

## Bundled resources

- `references/specification-checklist.md` — Detailed Dimension 1 audit checks.
- `references/best-practices-checklist.md` — Detailed Dimension 2 audit checks.
- `references/description-guide.md` — Detailed Dimension 3 audit guide.
- `references/common-issues.md` — Catalog of recurring problems and their fixes.
- `scripts/audit_skill.py` — Programmatic Dimension 1 checks (spec + body length).
- `assets/report-template.md` — The report structure to fill in for the user.

Read the relevant reference file before auditing in that dimension. Don't try to hold all four checklists in your head at once.

---

## Communicating with the user

Match the user's familiarity. Most users optimizing a skill know what YAML and frontmatter are; some don't. When in doubt:

- "frontmatter" / "kebab-case" → safe to use without definition.
- "trigger rate" / "eval" / "assertion" → brief definition on first use.
- "progressive disclosure" → worth a one-sentence definition; it's the central concept.

The user is iterating on an artifact they care about. Be direct about what's wrong and why. Don't pad the report with "great question!" — they want signal.
