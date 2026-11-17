## Description:

NotebookLM CLI wrapper via `node {baseDir}/scripts/notebooklm.mjs` for auth, notebooks, chat, sources, notes, sharing, research, and artifact generation/download.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fadeloo](https://clawhub.ai/user/fadeloo)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to run NotebookLM CLI workflows from an agent, including notebook management, chat, source handling, notes, sharing, research, and artifact generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated deletion, sharing, public access, export, and import commands can affect notebooks or expose content.

Mitigation: Verify notebook IDs, recipients, permissions, and account scope before running those commands.

Risk: NotebookLM notebooks may contain private, regulated, or business-sensitive material.

Mitigation: Review the skill before installing and avoid processing sensitive material unless the account and workflow are approved for that data.

## Reference(s):

- [NotebookLM CLI command catalog](references/cli-commands.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands execute through the local NotebookLM CLI and may produce files when artifact download or export commands are used.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
