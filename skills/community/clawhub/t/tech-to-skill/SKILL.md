---
name: tech-to-skill
description: |
  Distills technical long-form content (engineering notes, papers, project docs) into agent-callable skills with evidence indexing and temporal tracking. Use when the user wants to convert a technical article, paper, or project documentation into reusable skills that preserve engineering detail and traceability to source.
---

# tech-to-skill

Convert technical content into agent-callable skills that preserve enough detail to act on, trace back to source evidence, and record their own freshness.

## When to use

The user says things like:
- "Convert this engineering article into skills"
- "Distill this paper into a skill"
- "Extract development experience from project docs into skills"

## Input classification

Inspect the input. Follow the matching sub-skill's instructions:

| Input signal | Sub-skill |
|---|---|
| HTML/PDF long-form with chapters, code blocks, architecture discussion | [`longform-to-skill`](./sub-skills/longform-to-skill/SKILL.md) |
| Paper PDF or blog post with abstract/method/experiment structure | [`paper-to-skill`](./sub-skills/paper-to-skill/SKILL.md) |
| Git repo, ADR directory, retrospective docs, commit history | [`project-docs-to-skill`](./sub-skills/project-docs-to-skill/SKILL.md) |

The sub-skill files are reference documents for the executing agent, not separately invoked skills. Read the relevant sub-skill before starting Stage 1.

If the input doesn't clearly match one type, ask the user.

## Shared pipeline (4 stages)

1. **Structural Recognition** - Scan the source. Identify the author's own natural boundaries (headings, numbering, content transitions). Do NOT impose a preset structure.
2. **Extract** - Pull candidate units (each = a self-contained "how to do X" guidance). Show candidates to user for confirmation.
3. **Construct** - Fill What / How / Why + Evidence Index for each confirmed candidate. Create ref files for evidence.
4. **Validate** - Check structural completeness (What/How/Why present) and evidence accuracy (ref files point to real source content).

## Shared output contract

All sub-skills produce skills with this structure:

1. **What** - the problem this skill solves + trigger conditions + when NOT to use
2. **How** - the method, at a granularity the agent can act on (not abstract methodology)
3. **Why** - rationale from source + alternatives (if source discusses them) + timestamps
4. **Evidence Index** - pointers to source material, loaded on demand via progressive disclosure
5. **Timestamps** - `source_date`, `verified_date` (objective facts only, no guessed expiration)

See `templates/` for reference examples. Required: frontmatter fields, What/How/Why sections, Evidence Index. Format within each section is flexible.

## Shared description field constraint

The frontmatter `description` field is the agent's ONLY basis for triggering a skill. It must be concise and structured. Use this three-segment shape:

1. **Problem statement** (1 sentence) - what the skill solves
2. **Trigger condition** (1 sentence) - language signals the agent should match
3. **Adjacent skills** (optional, only if needed for disambiguation) - which other skills to consider instead, by name

Do NOT paste full "When NOT to use" content into description. Move that detail into the SKILL.md body. Do NOT include "Triggers on phrases like..." enumeration in description - those words belong in the body. The description is for activation; the body is for disambiguation.

Target length: under 600 characters. Concise is good, but the agent's ability to disambiguate between adjacent skills is more important than strict brevity.

This applies to all three sub-skills (longform, paper, project-docs) equally.

## Shared reference file naming convention

Every ref file must follow this exact format:

```
references/<skill-slug>-ref-<NN>.md
```

Where `<NN>` is a two-digit number (01, 02, ... 99), starting from 01 and continuous. The `<skill-slug>` prefix is the same as the skill directory name.

Strict rules:
- Always inside a `references/` subdirectory, never at skill root
- No suffix variants (forbidden: `ref-02-three-scenarios.md`, `ref-3.md`, `ref_a.md`)
- Two-digit zero-padding required (01, not 1)
- Sequential and gapless within each skill

This applies to all three sub-skills (longform, paper, project-docs) equally.

## Shared batch organization rule

Every distillation task (one execution of tech-to-skill, regardless of which sub-skill handled it) produces a **batch README.md** that lives in the same directory as the skills it describes. This README is task-level, not source-level: it documents what THIS distillation run produced, not what the source material contains.

The README must contain:
- Task scope: what source was distilled, what date, what tech-to-skill sub-skill ran
- Skills index table: skill name, source location, one-line topic
- Suggested reading order if skills have logical dependencies
- Validation status and known gaps
- Source coverage map (what was distilled, what was skipped, why)

This applies to all three sub-skills (longform, paper, project-docs) equally.

## Core principles

- **Faithful to source.** Only write what the source material contains. If the source doesn't discuss alternatives, write "Source does not discuss alternatives". Do NOT fabricate code, design rationale, or rejected approaches. Technical materials vary in completeness; skills must not pretend to be more complete than their source.
- **Preserve enough detail to act on.** Not abstract methodology, not line-number-fragile specifics. The right granularity is discovered by testing.
- **Every claim traces to evidence.** The agent can follow the Evidence Index to source material when the skill's guidance isn't enough.
- **No "vase" work.** Inter-skill links, glossary files, and other artifacts only exist if technically justified.
- **Objective timestamps.** Record `source_date` and `verified_date` as facts. Do not guess expiration windows.

## Sub-skills

- [`longform-to-skill`](./sub-skills/longform-to-skill/SKILL.md) - engineering notes / ebooks (Phase 1)
- [`paper-to-skill`](./sub-skills/paper-to-skill/SKILL.md) - papers / tech blogs (Phase 2)
- [`project-docs-to-skill`](./sub-skills/project-docs-to-skill/SKILL.md) - project development docs (Phase 3)
