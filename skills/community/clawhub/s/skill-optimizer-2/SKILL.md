---
name: skill-optimizer
description: Analyze the current conversation history and local installed skills to identify missed skill triggers, overlapping or duplicate skills, weak metadata, stale or risky skills, and workflow gaps. Generate a detailed audit report with evidence and present actionable items that the user can choose to fix, merge, delete, or keep and skip. Use this whenever the user wants to audit, optimize, clean up, consolidate, or improve skill triggering quality, skill metadata, skill safety, or skill installation workflow.
---

# Skill Optimizer

Audit the current thread and the locally visible skill set, then turn findings into a clear action queue that the user can review and choose from.

This skill is for governance and optimization, not for silently changing skills. Start with analysis, produce a report, and only edit files after the user chooses actions.

## Default Scope

Unless the user explicitly provides extra logs or transcript files, use:

- the current conversation history
- the current workspace's local skill directories
- installed skill directories that are directly visible from the environment

Do not claim global usage statistics unless the user provided cross-thread logs or telemetry.

## What To Look For

Audit for these issue types:

- `missed_trigger`
  A task in the current thread clearly matched an existing skill, but that skill was not used.
- `weak_metadata`
  `name` or `description` likely under-trigger because they miss common user phrasing or contexts.
- `duplicate_skill`
  The same skill, or near-identical copies, exist in multiple active places.
- `overlap_skill`
  Two or more skills cover nearly the same job and create ambiguity.
- `stale_skill`
  The skill description, instructions, bundled files, or `agents/openai.yaml` are out of sync.
- `risky_skill`
  The skill enables dangerous actions but lacks guardrails, warnings, or confirmation points.
- `install_flow_issue`
  The install, sync, backup, or directory workflow is confusing or inconsistent.
- `unused_candidate`
  Based on the current thread and local structure, a skill appears low-value or inactive. Phrase this carefully; it is not proof of never being used globally.

## Working Rules

Follow this sequence.

### Step 1: Inventory The Skills

Identify the skill roots that are relevant to the current workspace. Typical places include:

- `./.agents/skills`
- `./.claude/skills`
- project-local `skills/` directories
- directly relevant global skill directories if they are part of the current environment

For each skill, capture at least:

- path
- skill name
- description
- whether `agents/openai.yaml` exists
- whether bundled scripts or references exist

### Step 2: Read Current-Thread Evidence

Review the current conversation history and extract:

- the user's goals
- phrases the user used naturally
- where a skill was used
- where a skill should probably have been used but was not
- repeated confusion that suggests weak metadata or poor boundaries

Use exact evidence from the thread when possible, but keep quotations short.

### Step 3: Diagnose

Compare the thread evidence against the local skill inventory.

Pay special attention to:

- user phrasing that should have triggered a skill but did not
- skills with duplicate names or nearly identical descriptions
- skills whose body promises more than the bundled files support
- skills with risky capabilities and no explicit safety language
- local backup or fork directories that may confuse maintenance

### Step 4: Produce The Audit Report

Structure the report using the schema in [report-schema.md](./references/report-schema.md).

The report must include:

- executive summary
- findings grouped by issue type
- an action queue with one item per proposed intervention

Keep findings evidence-based. If something is an inference rather than a direct fact, say so.

### Step 5: Offer Only Four Actions

Every action item must expose exactly these user-facing actions:

- `Fix`
- `Merge`
- `Delete`
- `Keep and Skip`

Do not introduce extra action labels like `archive` or `disable` in the user-facing menu. If you internally think a "soft delete" is safer, explain that inside the recommendation, but keep the action menu limited to the four agreed options.

### Step 6: Wait Before Editing

Do not modify any skill during the audit step.

Only after the user selects action items should you:

- rewrite metadata
- sync `agents/openai.yaml`
- merge overlapping skills
- delete duplicates or obsolete skills

If the user selects `Delete`, confirm the exact target before removing files when there is any ambiguity.

## Recommendation Heuristics

Use these defaults unless the evidence strongly suggests otherwise:

- missed trigger or weak metadata -> recommend `Fix`
- duplicate or high-overlap skill copies -> recommend `Merge`
- clearly obsolete duplicates or user-rejected leftovers -> recommend `Delete`
- uncertain or disputed findings -> recommend `Keep and Skip`

For `unused_candidate`, be conservative. Prefer `Keep and Skip` or `Fix` over `Delete` unless the user explicitly wants aggressive cleanup.

## Report Style

- Be detailed, but not vague.
- Put findings before summaries.
- Make every action item independently understandable.
- Separate facts from recommendations.
- Use absolute file paths when referencing files.

## Output Contract

When running the audit, return:

1. A concise summary of the top themes
2. A detailed findings section grouped by category
3. An action queue using the schema in [report-schema.md](./references/report-schema.md)
4. A short prompt telling the user how to respond with their chosen actions

Example response pattern:

```md
Action Queue
- I01: Recommend `Fix`
- I02: Recommend `Merge`
- I03: Recommend `Keep and Skip`

Reply with selections such as:
- `I01 -> Fix`
- `I02 -> Merge`
- `I03 -> Keep and Skip`
```

## Boundaries

- Do not pretend the current thread represents all historical usage.
- Do not delete anything during analysis.
- Do not collapse separate findings into one vague item if the fixes differ.
- Do not overclaim certainty on "unused" skills.

## Bundled Resources

- [report-schema.md](./references/report-schema.md)
  Read this when drafting the audit report and action queue.
