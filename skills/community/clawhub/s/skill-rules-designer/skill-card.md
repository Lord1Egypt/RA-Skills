## Description:

Analyzes Claude Code skills and designs lossless restructuring plans for rules files, optional modules, templates, and clearer instructions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincentjiang06](https://clawhub.ai/user/vincentjiang06)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to restructure Claude Code skills into clearer, more modular rule files while preserving original content. It also supports A/B evaluation workflows for comparing skill versions and reviewing quality tradeoffs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to inspect and edit skill instruction files.

Mitigation: Review the proposed restructuring plan before approving writes, and keep backups or version control for skills being changed.

Risk: A/B evaluation mode can create additional workspace files and trigger multiple subagent runs.

Mitigation: Use evaluation mode only in workspaces where the extra artifacts and execution cost are acceptable.

## Reference(s):

- [JSON Schemas](references/schemas.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown plans and summaries, with optional JSON evaluation artifacts and file edits.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update skill files only after user confirmation; A/B evaluation mode can create extra workspace artifacts and run multiple subagents.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
