## Description:

Retrieve only relevant sections from Markdown memory, project notes, decision logs, and heading-structured knowledge bases with the mdselect CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevenybw](https://clawhub.ai/user/stevenybw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to recall prior context, decisions, preferences, and project history from specified or conventional Markdown memory locations while loading only relevant sections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on the mdselect CLI, which users may need to install manually.

Mitigation: Verify that mdselect is the intended package before installation and prefer isolated installation through pipx or uv tool.

Risk: The skill reads Markdown memory and notes that may contain sensitive context.

Mitigation: Use it only with Markdown memory or notes that are appropriate for the agent to read, and keep the workflow read-only.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/stevenybw/mdselect/tree/main/plugins/mdselect/skills/recall-markdown-memory)
- [ClawHub skill page](https://clawhub.ai/stevenybw/skills/recall-markdown-memory)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and cited source references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only workflow; output should cite selected Markdown source files and headings.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
