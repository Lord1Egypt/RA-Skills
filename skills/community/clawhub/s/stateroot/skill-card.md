## Description:

Installs and sets up StateRoot, a persistent multi-agent harness that carries shared identity, plans, tools, skills, memories, learnings, and project context across supported agent applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[usama04](https://clawhub.ai/user/usama04)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agent users use this bootstrap skill to install StateRoot and connect supported agent applications through its setup flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Linux and macOS setup pipes a mutable remote installer into a shell before authenticating it, so a compromised release could execute with the user's permissions.

Mitigation: Review the install method and consider waiting for a version-pinned installer with independently verifiable authentication.

Risk: The CLI has an uninstall-and-purge option that can delete user-global StateRoot data.

Mitigation: Review removal effects and use the purge option only when deleting that data is intended.

## Reference(s):

- [StateRoot homepage](https://stateroot.dev)
- [Installation guide](https://stateroot.dev/docs/getting-started/installation)
- [Setup guide](https://stateroot.dev/docs/getting-started/setup)
- [Privacy guide](https://stateroot.dev/docs/guides/privacy)
- [Troubleshooting FAQ](https://stateroot.dev/docs/reference/faq)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell command and PowerShell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may initiate installation and setup that modify user-level configuration and harness files; user confirmation is required.]

## Skill Version(s):

1.1.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
