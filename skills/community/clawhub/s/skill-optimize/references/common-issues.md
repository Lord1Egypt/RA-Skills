# Common Issues and Fixes

A catalog of recurring problems found when optimizing skills. Each entry: **the pattern** (what to look for), **why it matters** (the cost), and **the fix** (the change to make). Use this as a checklist while auditing — most skills exhibit 2–3 of these.

## 1. Vague verb syndrome

**Pattern**: Description says "Helps with X", "Processes X", "Manages X", "Deals with X". The body says things like "handles errors appropriately" or "follows best practices for X."

**Why it matters**: Vague verbs give the agent nothing to match against. The model already knows what "handle" and "process" mean — you're not adding signal. Triggering is poor because the description looks like every other skill's description.

**Fix**: Replace vague verbs with the specific operations. "Helps with PDFs" → "Extracts text and tables, fills forms, merges files." In the body, replace "handle errors appropriately" with the specific error-handling steps your project requires.

## 2. Generic "best practices" skill

**Pattern**: A skill that says "follow best practices for X" or "implement X correctly" without any project-specific facts. The body contains general advice that could apply to any project in the domain.

**Why it matters**: The agentskills.io guide is explicit: skills grounded in real expertise outperform ones synthesized from generic references. A generic skill doesn't pull its weight — the LLM can write that advice from general training data.

**Fix**: Either (a) make the skill project-specific by adding the schemas, conventions, edge cases, and gotchas from your actual codebase, or (b) admit the skill is redundant and remove it. Half-measures ("here are the official docs summarized") usually lose to no skill at all.

## 3. Kitchen-sink skill

**Pattern**: One skill that covers three or more unrelated domains. Common shape: a "developer utilities" skill that mixes database queries, API integrations, and deployment scripts.

**Why it matters**: A skill that activates for many unrelated tasks loads many unrelated instructions. The agent gets confused about which one to follow, and the skill fires on prompts where only a small slice is relevant.

**Fix**: Split into multiple skills, each with one coherent unit of work. A skill for "query the warehouse and format results" is fine. A skill that also does "administer the warehouse" should be two skills.

## 4. Tutorial instead of skill

**Pattern**: The body explains what a concept is before getting to the actionable part. "PDF (Portable Document Format) files are a common file format that contains text, images, and other content..." before "Use pdfplumber for extraction."

**Why it matters**: Tokens spent on background are tokens not spent on the instructions that actually matter. The agentskills.io guide: "Add what the agent lacks, omit what it knows." Explaining what a PDF is to an LLM wastes context and makes the skill harder to skim.

**Fix**: Cut all "what is X" intros. Start at the first actionable instruction. If a concept genuinely needs definition for the skill to make sense, define it inline in the smallest possible form (one sentence) and move on.

## 5. Bait description

**Pattern**: A description that lists every conceivable trigger keyword in a comma-separated list, hoping to match anything. "Skill for X, Y, Z, A, B, C. Use for foo, bar, baz, qux, quux."

**Why it matters**: This is overfitting to a specific query set, not a real triggering pattern. It bloats context, makes the description hard to read, and the keywords often look unnatural in a real user prompt.

**Fix**: Generalize. Find the *category* the listed keywords represent and describe that category. "Use for processing tabular data files like CSV, TSV, Excel" beats "Use for CSV, TSV, XLS, XLSX, parquet, AVRO, fixed-width, semicolon-delimited, tab-delimited..."

## 6. Missing gotchas

**Pattern**: A skill that doesn't list the non-obvious things the model would get wrong. Often a skill is "structurally correct" but every invocation produces the same mistake because the gotcha isn't documented.

**Why it matters**: The agentskills.io guide identifies gotchas as often the highest-leverage content. Every time you correct the agent in conversation, the correction should land in the gotchas section.

**Fix**: Add a "Gotchas" section. For each, write the non-obvious fact ("The `users` table uses soft deletes") and the consequence ("Queries must include `WHERE deleted_at IS NULL` or results include deactivated accounts"). Keep them in `SKILL.md`, not a reference file — the agent may not recognize when to load the reference.

## 7. No examples

**Pattern**: Output formats and edge cases are described in prose. "The output should be a JSON object with the user's name, email, and signup date, formatted as..."

**Why it matters**: LLMs pattern-match against concrete structures better than they follow prose descriptions. The same description with an example block produces more consistent output.

**Fix**: Add concrete examples. A 5-line code block showing the expected output format is worth a paragraph of prose. For edge cases, show a "before/after" or a "wrong/correct" pair.

## 8. Body too long

**Pattern**: `SKILL.md` body exceeds ~500 lines. Often a sign that detailed reference material is inlined.

**Why it matters**: The full body loads when the skill activates. Every line competes for the agent's attention with conversation history, system context, and other skills. Long bodies also make it harder for the agent to find the relevant instructions.

**Fix**: Move reference material to `references/` with explicit triggers. "Read `references/api-errors.md` if the API returns a non-200 status code" — not "see references/ for details." Keep the body focused on the core workflow; offload the details.

## 9. Missing `allowed-tools` declaration

**Pattern**: The skill uses Bash, but the user hasn't approved the specific commands. Each invocation triggers a permission prompt.

**Why it matters**: Friction. The user gets prompted for every Bash call the skill makes.

**Fix**: For Claude Code and similar, add `allowed-tools` to the frontmatter with the specific tool patterns the skill needs. Example: `allowed-tools: Bash(git:*) Bash(jq:*) Read Write`. Note this field is experimental per the spec — support varies.

## 10. Description too short

**Pattern**: Description is one line, no "use this when" context, no keyword list. Often a description of just "Helps with X" or a single action verb.

**Why it matters**: Under-triggering. The description doesn't tell the agent when to reach for the skill, so the agent only activates it on the most literal matches.

**Fix**: Add the "Use this skill when..." pattern. List 2–3 specific trigger contexts. Include the pushy catch-all at the end: "even if the user doesn't explicitly mention 'X' or 'Y'."

## 11. Description over 1024 chars

**Pattern**: Description hits the spec limit. Often because someone tried to enumerate every possible trigger keyword.

**Why it matters**: Validation fails. The skill won't load on some clients. Even on lenient clients, the description is bloated and slow to scan.

**Fix**: Generalize. Replace keyword lists with category descriptions. Cut redundant phrases ("This skill is designed to..."). Aim for 200–500 chars typically; only go higher when the skill genuinely covers a wide scope.

## 12. Name mismatch with directory

**Pattern**: The `name` in frontmatter doesn't match the parent directory name.

**Why it matters**: Hard spec rule. Some clients will silently fail to load the skill or load the wrong one.

**Fix**: Decide on one name and apply it consistently. If the directory is `pdf-processing/` and the frontmatter says `pdf`, pick one — usually the directory name is the source of truth, and the frontmatter should be edited to match.

## 13. Underscored or camelCase name

**Pattern**: `name: pdf_processing` or `name: pdfProcessing` in frontmatter.

**Why it matters**: Spec rule — names must be kebab-case. Validation will fail.

**Fix**: Rename. `pdf_processing` → `pdf-processing`. Update the directory name to match. Verify no other files reference the old name.

## 14. Multiple `---` fences in the file

**Pattern**: File starts with `---`, has the frontmatter, closes with `---`, but then contains another `---` somewhere later (a horizontal rule in the body, or a code fence in a YAML example).

**Why it matters**: Some validators match the frontmatter with a non-greedy regex and stop at the first `---` they see after the opening, which is the second fence. The "real" frontmatter is then misread or the body is treated as frontmatter.

**Fix**: Replace any `---` in the body with `***` or another horizontal rule marker. The frontmatter must contain exactly one opening and one closing fence.

## 15. The "obvious" answer

**Pattern**: A skill whose body is essentially "do the right thing" — instructions so generic they could be replaced by "be helpful and accurate."

**Why it matters**: Adds no signal. The LLM would have done the right thing (or close to it) without the skill.

**Fix**: If the skill exists to remind the model of conventions the model already knows, delete it. If it exists to capture project-specific facts, fill in those facts — the project schemas, the gotchas, the specific tools. The skill is the place for *non-obvious* knowledge, not for reaffirming what the model already does well.

## 16. Bundle bloat

**Pattern**: A skill that drags in large binary assets, sample data files, full PDF documentation, or dozens of supporting files. The agentskills.io spec keeps `SKILL.md` under 500 lines precisely because of context cost, and runtime platforms like OpenClaw impose hard caps (e.g. 50MB total bundle, ~40 non-markdown files).

**Why it matters**: Every byte is a token-cost question once the skill loads. Reference docs that ship inside the skill are usually available on the web; sample data is usually reproducible; large assets trigger overlong context and slow activation. Most of the time, the user has the same access to the upstream source.

**Fix**: Keep the bundle small and text-only. A useful rule of thumb — for every file in the skill, ask: would a future reader know how to get this from the original source in one click? If yes, link instead of bundling. If you must bundle, the file should be **non-redundant** (not duplicated from upstream) and **small enough** to inline into the body if it's ever needed. Drop large assets and binary files entirely.

## 17. Declared-scope drift

**Pattern**: The description says one thing; the body does another. Example: description says "Convert Markdown to PDF", but the body also covers writing/editing Markdown, linting, and pre-processing frontmatter. Or: description says it works offline, but the body silently relies on a network call.

**Why it matters**: The description is the *contract* the agent uses to decide whether to activate the skill. If the body extends beyond the contract, the skill will produce outputs the user didn't ask for, and platforms that audit declaration-vs-behavior (e.g. security scanners on skill registries) will flag it as a mismatch. Trust breaks.

**Fix**: Keep description and body aligned. If the body needs to grow, update the description. If the description needs to be honest about scope, narrow the body. Two specific tactics:
- Add a "What this skill does NOT do" line to the description when adjacent domains are tempting.
- If the body legitimately covers two domains, split the skill (see Kitchen-sink skill above).

## 18. Hidden costs and credentials

**Pattern**: The body tells the model to call an external service (LLM API, paid SaaS, cloud GPU) without noting that doing so costs money, requires an account, or needs a specific API key. The skill "just works" on the author's machine and breaks (or quietly bills the user) for everyone else.

**Why it matters**: Users get surprised. Either the skill fails to run (no API key) or it costs more than they expected. The first is annoying; the second is a billing violation.

**Fix**: In the description or at the top of the body, declare: (a) which external services the skill touches, (b) what credentials/API keys are required, (c) what the cost structure looks like (per-call, per-token, per-month). Use the `compatibility` frontmatter field for environment requirements, and the body for usage caveats. If the skill needs an env var the user hasn't set, fail loudly with a clear error message, not a vague stack trace.
