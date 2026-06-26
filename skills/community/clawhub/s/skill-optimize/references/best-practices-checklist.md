# Best Practices Checklist

Use this when running the **Dimension 2** (Best Practices) audit. Source: [agentskills.io/skill-creation/best-practices](https://agentskills.io/skill-creation/best-practices). Unlike the spec, these are not binary — give each a **Pass / Warning / Fail** verdict with one-sentence evidence.

## Scope

- [ ] **One coherent unit of work.** A skill that does two unrelated things should be split. A skill for "querying a database and formatting the results" is fine. A skill that also covers "database administration" is over-scoped.
- [ ] **Composable with other skills.** If activating this skill for one task forces loading of unrelated instructions, the scope is wrong.
- [ ] **Activates precisely.** A skill so broad it could match half of all user requests will fire too often. If the description could match many unrelated domains, narrow the scope.

## Specificity calibration

- [ ] **Flexible instructions for flexible tasks.** Code review, drafting, brainstorming — these tolerate variation. Use prose and reasoning, not ALWAYS/NEVER.
- [ ] **Prescriptive instructions for fragile tasks.** Database migrations, security checks, anything destructive — give the exact sequence, even the exact command. Explain *why* each step matters.
- [ ] **No reflexive rigidity.** If you find yourself writing `ALWAYS` or `NEVER` in all caps for a non-fragile step, that's a yellow flag. Either the rule is more flexible than you think, or the underlying *reason* should be explained instead.
- [ ] **Reasoning, not just rules.** "Use parameterized queries to prevent SQL injection" works better than "ALWAYS use parameterized queries." Models that understand the *why* make better context-dependent calls.

## Defaults, not menus

- [ ] **One default is named explicitly.** When multiple tools or approaches could work, the skill should pick one and say "use X."
- [ ] **Alternatives are mentioned briefly as escape hatches**, not presented as equal choices. "For scanned PDFs requiring OCR, use pdf2image with pytesseract instead" — not "You can use pypdf, pdfplumber, PyMuPDF, or pdf2image."

## Procedure over declaration

- [ ] **Teaches a method, not an answer.** "Read the schema, join on `_id` foreign keys, apply filters, aggregate" is reusable across queries. "Join `orders` to `customers` on `customer_id`, filter where `region = 'EMEA'`, sum `amount`" only works for one query.
- [ ] **Output format templates count as procedure**, not declaration. A template the agent can pattern-match against is fine; a single hard-coded answer is not.
- [ ] **Constraints are explicit** — "never output PII", "always include the date" — these are procedure-level rules the agent should follow across instances.

## Gotchas

- [ ] **Has a gotchas section** (or equivalent). This is often the highest-leverage content in a skill — non-obvious, environment-specific corrections.
- [ ] **Gotchas are concrete**, not generic. "Handle errors appropriately" is a non-gotcha. "The `users` table uses soft deletes — queries must include `WHERE deleted_at IS NULL`" is a gotcha.
- [ ] **Gotchas live where the agent reads them first**, i.e., in `SKILL.md`, not buried in a reference file. (The agentskills.io guide is explicit: the agent may not recognize the trigger to load a reference file for a non-obvious issue.)

## Output templates

- [ ] **When the output has a specific shape, a template is provided.** Concrete structures pattern-match better than prose.
- [ ] **Templates live in `SKILL.md` for short forms**, in `assets/` for long ones (referenced from `SKILL.md` with a clear "use this template when..." trigger).

## Progressive disclosure

- [ ] **`SKILL.md` body stays under ~500 lines.** Long content moves to `references/` or `assets/`.
- [ ] **References tell the agent when to load them.** "Read `references/api-errors.md` if the API returns a non-200 status" is useful. "See references/ for details" is not.
- [ ] **File references are one level deep.** No `references/foo/bar/baz.md` chains.
- [ ] **No "kitchen sink" `SKILL.md`** that tries to be the entire knowledge base for a domain.

## Token budget

- [ ] **Adds what the agent lacks, omits what it knows.** The skill is not the place to explain what a PDF is, how HTTP works, or what a database migration does.
- [ ] **No "what is X" intros** before the actual instructions. Jump straight to the actionable content.
- [ ] **Cut sentences the agent could write itself.** If removing a paragraph wouldn't change the agent's output, remove it.
- [ ] **One working example beats three paragraphs of explanation.** A code block or sample output carries more signal than the equivalent prose.

## Reusable scripts

- [ ] **Repeated work is bundled.** If a test transcript shows the agent independently writing the same helper logic across runs, the skill should bundle a tested script in `scripts/` and tell the agent to use it.
- [ ] **Scripts are self-contained or document their dependencies** in a header comment.
- [ ] **Scripts include helpful error messages** — bad inputs should fail loudly, not silently.

## Validation loops

- [ ] **For multi-step workflows, the skill has a self-check step.** "After filling the form, run `scripts/verify.py`" or "Confirm the output contains X before finalizing."
- [ ] **For batch/destructive operations, plan-validate-execute is used.** Extract → map → validate against source of truth → execute.

## How to score

After going through the checklist, give the user:

- **Per-axis verdict**: Pass / Warning / Fail with one sentence of evidence.
- **Top 3 improvements**: The three changes that would most improve the skill, ranked by leverage. Don't try to fix everything at once.
- **Skip the rest**: If a finding is technically true but won't change the agent's behavior, say so and move on. Signal beats completeness.
