---
name: spec-to-adr
description: >-
  Convert agent execution plans into MADR-format Architecture Decision Records
  for audit trails and architecture progression. Use when the user asks to
  create an ADR, record an architectural decision, document a plan as a
  decision record, or convert a spec/plan into an ADR. Supports GSD phase
  plans, Cursor CreatePlan output, and generic markdown plans.
---

# spec-to-adr

Convert execution plans into numbered MADR Architecture Decision Records stored in `docs/adr/`.

## Workflow

Follow these steps in order:

1. **Locate the plan** -- identify the source plan using the detection rules below.
2. **Extract decisions** -- pull structured data from the plan into MADR fields.
3. **Generate the ADR** -- write the file using the template in [references/madr-template.md](references/madr-template.md).
4. **Update the index** -- append an entry to `docs/adr/README.md`.
5. **Report** -- show the user the ADR path, number, and a one-line summary.

## Step 1: Locate the Plan

Determine the plan format by checking in this order:

### GSD Phase Plan

Present when any of these exist relative to the workspace root:

- `.planning/phases/*/PLAN.md`
- `.planning/ROADMAP.md`
- `.planning/phases/*/RESEARCH.md`

Use the most recent `PLAN.md` unless the user specifies a phase. If multiple phases exist, ask which one to record.

### Cursor CreatePlan

A `.plan.md` file (often in `.cursor/plans/`) with this structure:

- YAML frontmatter containing `name`, `overview`, and `todos`
- Markdown body with headings describing the approach

### Generic Markdown Plan

Any markdown document the user points to that contains:

- A problem or goal statement
- One or more approaches, options, or alternatives
- A chosen direction or recommendation

If the user says "create an ADR" without pointing to a plan, ask: "Which plan or decision should I record? Point me to a file, or describe the decision."

## Step 2: Extract Decisions

Map plan content to MADR fields. Not every field will have a direct source -- infer where reasonable, leave blank with a `TODO` marker where not.

| MADR Field | GSD Plan Source | CreatePlan Source | Generic Source |
|---|---|---|---|
| Title | Phase name / goal | `name` from frontmatter | First H1 or user-provided |
| Context and Problem | `RESEARCH.md` problem section, or `PLAN.md` overview | `overview` from frontmatter | Opening paragraphs or problem statement |
| Decision Drivers | Constraints, requirements from RESEARCH | Trade-offs discussed in body | Bullet lists of requirements or constraints |
| Considered Options | Alternative approaches in RESEARCH or PLAN | Multiple approaches in body sections | Sections describing different options |
| Decision Outcome | The chosen plan/approach in PLAN.md | The plan body (the chosen path) | The recommended or selected approach |
| Consequences | Risk sections, known trade-offs | Noted risks or caveats | Stated pros/cons of chosen path |

### Extraction guidelines

- Preserve the plan's original language where possible; do not over-paraphrase.
- If the plan only describes one option (the chosen path) with no alternatives, set "Considered Options" to just that option and note in "More Information" that no alternatives were documented.
- For GSD plans with a `VERIFICATION.md`, pull verification criteria into Consequences.
- For CreatePlan todos, summarize them under "Decision Outcome" as the implementation approach.
- Always populate "More Information" with a relative link back to the source plan file.

## Step 3: Generate the ADR

### Numbering

1. List existing files in `docs/adr/` matching the pattern `NNNN-*.md`.
2. Find the highest number. If no ADRs exist, start at `0001`.
3. Increment by 1. Pad to 4 digits.

### Filename

`NNNN-kebab-case-title.md` where the title is derived from the decision title, lowercased, spaces replaced with hyphens, non-alphanumeric characters removed, truncated to 60 characters.

### Content

Read [references/madr-template.md](references/madr-template.md) and fill in the extracted fields. Rules:

- **Status**: default to `accepted`. If the user says the decision is still under review, use `proposed`.
- **Date**: use today's date in `YYYY-MM-DD` format.
- **Decision-makers**: use the git user name (`git config user.name`) if available, otherwise leave as `TODO`.
- **Consulted / Informed**: leave as `TODO` unless the user specifies.
- Omit empty optional sections rather than leaving placeholder text, except for "More Information" which must always link to the source plan.

### Output location

Write to `docs/adr/NNNN-kebab-case-title.md`. Create the `docs/adr/` directory if it does not exist.

If the user has a different ADR directory convention (check for existing `adr/`, `doc/adr/`, `architecture/decisions/`), use that instead.

## Step 4: Update the Index

Maintain a `docs/adr/README.md` that lists all ADRs. If it does not exist, create it using the template in [assets/adr-index-template.md](assets/adr-index-template.md).

Append a row to the table:

```
| NNNN | Title | accepted | YYYY-MM-DD |
```

## Step 5: Report

After writing the ADR, tell the user:

- The file path (e.g., `docs/adr/0003-use-postgres-for-persistence.md`)
- The ADR number
- A one-sentence summary of the recorded decision
- Remind them they can change the status later (`proposed`, `deprecated`, `superseded by ADR-NNNN`)

## Edge Cases

- **Multiple decisions in one plan**: If a plan contains several distinct architectural decisions, ask the user whether to create one ADR per decision or a single combined ADR. Default to one-per-decision.
- **Superseding an existing ADR**: If the user says this decision replaces a previous one, set the new ADR status to `accepted` and update the old ADR's status to `superseded by ADR-NNNN`.
- **Thin plans**: If the source plan is too brief to populate most MADR fields, generate what you can and mark sparse sections with `<!-- TODO: fill in after implementation -->`. Warn the user the ADR is incomplete.
- **No docs/adr/ directory**: Create it. Do not ask for permission -- this is a standard convention.
