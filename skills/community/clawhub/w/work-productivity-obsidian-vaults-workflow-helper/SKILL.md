---
name: work-productivity-obsidian-vaults-workflow-helper
description: Work with Obsidian-style Markdown vaults and local knowledge bases. Use when the user needs to organize notes, add frontmatter, repair links, design vault workflows, create templates, migrate Markdown, or automate safe local note maintenance.
---

# Work Productivity Obsidian Vaults Workflow Helper

Use this skill when a user wants their notes to remain plain Markdown while still gaining structure, repeatable workflows, and safe automation.

Read `references/requirement-plan.md` for the demand evidence and original planning criteria.

## Vault Intake

Gather or infer:

- Vault root path and any folders that must not be edited.
- Note naming conventions, frontmatter schema, tags, aliases, and link style.
- Whether attachments, canvases, daily notes, tasks, or dataview queries are in scope.
- Desired output: cleanup plan, template set, migration, index note, or automation script.

## Workflow

1. Inspect the vault layout before recommending changes.
2. Separate read-only analysis from file mutations; propose a dry-run summary for bulk edits.
3. Normalize metadata carefully: preserve existing YAML keys, note aliases, timestamps, and user formatting unless the user asks otherwise.
4. Repair links and backlinks using vault-relative paths; avoid breaking embeds and attachments.
5. Produce templates or scripts only when the repeated workflow justifies them.
6. Verify by sampling changed notes and checking for unresolved wiki links, duplicate tags, or malformed frontmatter.

## Guardrails

- Never rewrite a whole vault blindly.
- Avoid cloud-only sync assumptions; keep procedures local-file friendly.
- Prefer reversible changes, backups, or generated patch plans for large migrations.
- Treat personal notes as sensitive content; summarize structure without exposing private text unnecessarily.

## Outputs

- Vault audit with risks and recommended structure.
- Markdown templates for notes, projects, meetings, or daily logs.
- Frontmatter migration plan or script.
- Link repair and index-building checklist.

## Validation Checklist

- Paths and excluded folders are explicit.
- Bulk edits have a dry-run or rollback path.
- Markdown, YAML frontmatter, links, and attachments remain valid.
- The workflow fits Obsidian without requiring proprietary storage.

## Triggers

Keywords: Obsidian, vault, Markdown notes, frontmatter, backlinks, wiki links, dataview, daily notes, knowledge base.

Example requests:

- `Clean up my Obsidian vault without breaking links.`
- `Use $work-productivity-obsidian-vaults-workflow-helper to add frontmatter templates to these notes.`
- `Plan a migration from loose Markdown files into an Obsidian vault.`
