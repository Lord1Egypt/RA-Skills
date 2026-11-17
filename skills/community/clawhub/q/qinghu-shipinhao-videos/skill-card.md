## Description:

Retrieves a WeChat Channels account's published videos through Qinghu AI, with cursor-based pagination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and marketing analysts use this skill to retrieve and review a WeChat Channels account's published videos, including additional pages when available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install or upgrade Node.js and the qhkit package in the user's environment.

Mitigation: Review installation steps before execution; prefer a preinstalled, version-pinned qhkit.

Risk: Configuring an API token through shell commands or persistent local settings may expose credentials.

Mitigation: Supply credentials through the platform's secret manager instead of shell commands or persistent local configuration.

Risk: Video-list lookups use paid API calls that consume Qinghu credits.

Mitigation: Check the current estimate and obtain user approval before paid calls.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-shipinhao-videos)
- [Qinghu qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise response with video-list data and optional table file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports cursor pagination; reports credits consumed for paid calls.]

## Skill Version(s):

0.1.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
