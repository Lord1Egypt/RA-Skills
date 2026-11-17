## Description:

Task manager for AI agents. Works instantly - no account, no phone needed. 19 tools for nested task trees, batch ops, local storage, optional phone sync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[banonanon](https://clawhub.ai/user/banonanon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to add a SHrimp MCP task manager that can create, search, update, organize, batch, and sync nested task trees for agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs an external npm package through npx.

Mitigation: Install only if you trust the SHrimp npm package and publisher, and review npm package source or provenance before execution where appropriate.

Risk: Paired mode can read or modify prompt and provider settings, activity logs, inbox items, and synced task data.

Mitigation: Use local mode when sync is not needed, and enable paired mode only for accounts and devices where that access is acceptable.

Risk: Local mode stores task data under ~/.shrimp/tasks.json and sends a disclosed anonymous daily usage ping.

Mitigation: Review local storage expectations and privacy disclosure before use, especially on shared machines or sensitive workflows.

## Reference(s):

- [SHrimp Homepage](https://hermitshell.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and MCP tool descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [MCP integration exposing local and paired task-management tools]

## Skill Version(s):

1.0.7 (source: server release metadata; artifact frontmatter lists 1.0.6)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
