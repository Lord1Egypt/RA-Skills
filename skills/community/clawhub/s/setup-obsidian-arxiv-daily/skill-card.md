## Description:

Use when installing, migrating, updating, validating, troubleshooting, or scheduling an automated arXiv paper digest inside an Obsidian Vault on Windows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[debtvc2022](https://clawhub.ai/user/debtvc2022)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users use this skill to install or update a Windows-based Obsidian arXiv digest, configure approved collection settings, validate the installed copy, and optionally schedule the daily run.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A scheduled daily task can repeatedly read arXiv results, write generated notes and logs inside the selected Obsidian Vault, and archive old generated paper notes.

Mitigation: Review the target Vault, project name, task name, and schedule before approval; use dry-run and WhatIf validation before registering or replacing a task.

Risk: When summaries are enabled and DEEPSEEK_API_KEY is present, paper titles, authors, and abstracts may be sent to DeepSeek.

Mitigation: Keep credentials in the process environment only, review summary settings before use, and disable summaries when external summarization is not acceptable.

Risk: Forceful update or task replacement can overwrite packaged workflow files or replace an existing scheduled task.

Mitigation: Require explicit approval after inspecting the existing project or task, and preserve generated papers, daily notes, archives, logs, and credentials.

## Reference(s):

- [Operations Reference](references/operations.md)
- [ClawHub Skill Page](https://clawhub.ai/debtvc2022/skills/setup-obsidian-arxiv-daily)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with PowerShell and Python commands plus configuration edits.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The installed workflow produces Obsidian Markdown notes, dashboard content, logs, and optional Windows scheduled task configuration.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
