---
name: support-template-multilang-sync
description: Update multilingual customer support reply templates in markdown files, then sync the updated content to Feishu Wiki, log the change in a GitHub issue, and package/publish the repeatable workflow to ClawHub. Use when maintaining files like kb-templates/common-responses.md, adding new languages, normalizing template structure, or turning a one-off support content update into a reusable skill.
---

# Support Template Multilang Sync

## Overview

Use this skill to carry one support-template update through four outputs without losing consistency: the source markdown file, the Feishu Wiki knowledge base, the GitHub change log issue, and a reusable ClawHub skill.

Keep the file update authoritative. Derive the Wiki page body and GitHub issue summary from the final file contents instead of maintaining separate versions by hand.

## Workflow

1. Read the target template file and identify its current structure.
2. Add or revise language sections while preserving placeholders such as `{{ticket_id}}`.
3. Re-read the file and verify each response block has the expected languages and no placeholder drift.
4. Sync the finalized content to Feishu Wiki.
5. Create a GitHub issue that records what changed, which file changed, and what follow-up is needed.
6. Update this skill if the process or API assumptions improved.
7. Package the skill and publish it to ClawHub when credentials are available.

## File Update Rules

- Preserve the existing response categories unless the user asked to rename or reorder them.
- Keep all variables exactly unchanged, including braces and capitalization.
- Keep tone consistent across languages: support-safe, polite, operationally clear.
- Prefer one repeated structure per response block, for example `### English`, `### Chinese`, `### French`, `### Korean`.
- If only one section was multilingual before, consider normalizing the rest if that makes future maintenance safer.

## Verification Checklist

After editing the markdown file, check all of the following:

- Every response section has the same language set.
- Existing languages were not accidentally modified beyond necessary normalization.
- Placeholders such as `{{ticket_id}}` are present in every language where required.
- Bullet lists remain aligned across languages.
- Headings render cleanly in markdown.

## Feishu Wiki Sync

Use Feishu as the published knowledge-base mirror.

Preferred approach:
- Use the final markdown file as the content source.
- Create or update the target Wiki page under the customer-support knowledge base.
- Include a short update note at the top: date, source file, newly added languages.

Operational requirements:
- Need `FEISHU_ACCESS_TOKEN` or the pair `FEISHU_APP_ID` + `FEISHU_APP_SECRET`.
- Need `FEISHU_WIKI_SPACE_ID` and usually a parent node token.
- If permissions fail with `99991672`, stop and resolve app permissions before retrying.

## GitHub Issue Logging

Create one issue per template update batch.

Include:
- Title that names the template and languages added.
- Source file path.
- Summary of what was changed.
- Wiki sync status.
- Any blockers or follow-up tasks.

Suggested title pattern:
- `Update common support response templates with French and Korean`

## ClawHub Packaging and Publish

Keep the skill lean and practical.

Required contents:
- `SKILL.md` with trigger-oriented description.
- Optional helper script(s) only if they remove repeated manual work.
- Optional references for API steps or publishing notes.

Before publishing:
- Run the packaging script from the OpenClaw `skill-creator` skill.
- Fix validation issues before retrying.
- Publish with `clawhub publish <skill-folder>` when authenticated.

## Resources

### scripts/
- `prepare_issue_body.py`: generate a compact GitHub issue body from the finalized markdown file and change metadata.

### references/
- Add environment or API notes only if the workflow becomes more complex. Keep this skill small by default.
