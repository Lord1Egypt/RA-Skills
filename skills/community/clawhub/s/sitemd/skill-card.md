## Description:

Build and manage websites from Markdown. Create pages, generate content, configure settings, and deploy -- all through MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tyler-berggren](https://clawhub.ai/user/tyler-berggren)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site maintainers use this skill to create, configure, validate, build, and deploy Markdown-based websites through an agent using sitemd MCP tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install and run a downloaded sitemd binary that is not independently reviewed in the artifact.

Mitigation: Use it only from a trusted distribution channel and verify the binary source and update path before installation.

Risk: The skill can modify and deploy websites, including production-impacting changes.

Mitigation: Confirm destructive, activation, deployment, and production changes before running them.

Risk: Magic links, API keys, and SITEMD_TOKEN are sensitive credentials.

Mitigation: Treat authentication links and tokens as secrets, limit credential scope where possible, and avoid broad account credentials unless necessary.

## Reference(s):

- [sitemd homepage](https://sitemd.cc)
- [ClawHub skill page](https://clawhub.ai/tyler-berggren/skills/sitemd)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with tool names, file paths, shell commands, and configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct an agent to create or modify website content, settings, theme files, media, built output, deployment state, authentication state, and API keys.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
