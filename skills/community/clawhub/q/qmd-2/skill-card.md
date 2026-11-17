## Description:

Search markdown knowledge bases, notes, and documentation using QMD.

This skill is ready for commercial/non-commercial use.

## Publisher:

[satvik374](https://clawhub.ai/user/satvik374)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and knowledge workers use this skill to search local Markdown notes, documentation, and knowledge bases through QMD CLI or MCP workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: QMD can index private Markdown notes or documentation if sensitive folders are added to a collection.

Mitigation: Add only intended Markdown directories to QMD collections and avoid indexing sensitive folders unnecessarily.

Risk: The skill depends on installing and running the third-party @tobilu/qmd package.

Mitigation: Pin or otherwise verify the @tobilu/qmd package before global installation.

Risk: The optional local HTTP daemon exposes QMD query access as a background service.

Mitigation: Run HTTP daemon mode only when needed and keep access local or otherwise controlled.

## Reference(s):

- [QMD MCP Server Setup](artifact/references/mcp-setup.md)
- [ClawHub Skill Page](https://clawhub.ai/satvik374/skills/qmd-2)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include QMD query structures, MCP setup guidance, CLI commands, and local HTTP API examples.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
