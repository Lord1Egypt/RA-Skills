# Description Optimization Guide

Use this when running the **Dimension 3** (Description) audit. Source: [agentskills.io/skill-creation/optimizing-descriptions](https://agentskills.io/skill-creation/optimizing-descriptions). The description is the **only** thing the agent sees before deciding whether to activate the skill — it carries the entire triggering burden.

## How triggering actually works

Agents load skills via progressive disclosure. At startup, they read only `name` + `description` for every available skill. When a user's task matches a description, the agent reads the full `SKILL.md`. If the description doesn't convey when the skill is useful, the agent won't reach for it.

One important nuance: agents typically only consult skills for tasks that require knowledge or capabilities beyond what they can handle alone. A simple, one-step request like "read this PDF" may not trigger a PDF skill even if the description matches perfectly — the agent can handle it directly. The descriptions matter most for **non-trivial, specialized, multi-step** work.

This means a "perfect" description can't force triggering. It can only make the right prompts clearly relevant and the wrong prompts clearly irrelevant. Audit accordingly — the goal is *precision*, not raw hit rate.

## Anatomy of a good description

A good description has three components, in order:

1. **What the skill does** — the concrete operations it performs. Verbs, not nouns.
2. **When to use it** — the user intent and context that should trigger activation. Imperative phrasing.
3. **Pushy coverage** — explicit mention of cases where the user doesn't name the domain directly. This catches the near-misses.

```yaml
# Good
description: Extracts text and tables from PDF files, fills PDF forms, and merges multiple PDFs. Use when working with PDF documents or when the user mentions PDFs, forms, or document extraction.

# Bad
description: Helps with PDFs.
```

## Audit checks

For each, give Pass / Warning / Fail with evidence.

### Structure

- [ ] **Imperative framing.** "Use this skill when..." not "This skill does..." The agent is deciding whether to *act*, so tell it when to act.
- [ ] **User intent over implementation.** Describes what the user is trying to achieve, not the skill's internal mechanics. "Analyze CSV files" beats "Loads CSVs into pandas, runs describe(), plots with matplotlib."
- [ ] **Both WHAT and WHEN present.** A description that's only "what" (e.g., "Extracts PDF text") under-triggers. One that's only "when" (e.g., "Use when working with documents") over-triggers.

### Pushiness

- [ ] **Lists specific contexts where the skill applies.** Not "in various situations" — actual scenarios with concrete details.
- [ ] **Catches the near-misses.** Includes cases where the user doesn't name the skill's domain directly: "even if they don't explicitly mention 'CSV' or 'analysis'."
- [ ] **No vague verbs.** "Helps with", "handles", "deals with", "manages", "processes" — replace with the specific operation.

### Keywords

- [ ] **Concrete, specific terms the user would type.** File types (`pdf`, `csv`, `xlsx`), domain names (`Stripe`, `Salesforce`), action verbs (`extract`, `merge`, `clean`).
- [ ] **Avoids generic verbs as primary signal.** "Process" tells you nothing. "Convert PDF to markdown" tells you a lot.
- [ ] **Includes alternate phrasings the user might use.** "Reschedule a meeting" and "move a calendar event" both describe the same intent.

### Length

- [ ] **Under 1024 chars.** (Spec limit, hard.)
- [ ] **Not padded.** A few sentences to a short paragraph is the sweet spot. If you're over 800 chars, you're probably trying to enumerate every possible trigger — generalize instead.
- [ ] **No redundant phrases.** Cut "This skill is designed to", "The purpose of this skill is". Just say what it does.

### Mechanics

- [ ] **No angle brackets.** Spec rule, fails validation.
- [ ] **No newline-only structure that breaks YAML.** Multi-line is fine; quote it properly.
- [ ] **Doesn't start with "I" or "This skill".** Start with the verb or the user context.

## Concrete rewrites

These come up a lot. The pattern is the same: vague verb → specific verbs, missing trigger context → explicit "use this when".

| Before | After | Why |
|---|---|---|
| `Helps with PDFs.` | `Extracts text and tables from PDF files, fills PDF forms, and merges multiple PDFs. Use when working with PDF documents or when the user mentions PDFs, forms, or document extraction.` | Specific verbs, explicit triggers, includes keyword list. |
| `Process CSV files.` | `Analyze CSV and tabular data files — compute summary statistics, add derived columns, generate charts, and clean messy data. Use this skill when the user has a CSV, TSV, or Excel file and wants to explore, transform, or visualize the data, even if they don't explicitly mention "CSV" or "analysis".` | Adds what the skill does *to* the CSV, names the trigger contexts, ends with the pushy catch-all. |
| `Create documents.` | `Generate Word documents (.docx) from structured data — merge templates, fill in fields, apply styles. Use when the user asks to create, generate, or export a Word or .docx file, or wants to automate document generation from JSON or CSV.` | Names the file type explicitly, lists user verbs, gives the data source patterns. |
| `Skill for debugging.` | `Diagnose and fix bugs in Python code — read stack traces, reproduce failures, form and test hypotheses, apply targeted fixes. Use this skill when the user reports a bug, shares an error or traceback, asks "why is X failing", or wants help making failing tests pass.` | Specific operations, list of trigger phrasings the user would actually type. |

## Description optimization loop (if the user wants to verify)

This skill audits the *wording*. To verify the description actually triggers correctly, defer to `skill-creator` — its description-optimization loop is purpose-built for this. The short version:

1. Write **~20 eval queries** — 8–10 that *should* trigger, 8–10 that *should not*. Include near-misses in the "should not" set (e.g., "update a formula in Excel" for a CSV-analysis skill).
2. **Split 60/40** into train and validation. The split is fixed across iterations.
3. **Run each query 3 times** to get a trigger rate (model behavior is non-deterministic).
4. **Revise the description** based on the train-set failures. Avoid adding specific keywords from failed queries — that's overfitting. Generalize to the category instead.
5. **Pick the best iteration by validation pass rate**, not train. Train is what you optimized against; validation is the honest test.

But for most cases, the audit and the rewrites in this guide are enough. Only run the loop if the user reports triggering is genuinely broken in production.

## Output

The Dimension 3 section of the report should contain:

- A list of audit findings (Pass / Warning / Fail per check).
- A **proposed rewrite** of the description, with a one-sentence explanation of *why* each change improves triggering.
- An **optional eval query set** (5–10 mixed should/should-not-trigger queries) the user can run through `skill-creator` if they want to verify.

Don't ship the new description without showing the diff.
