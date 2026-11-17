## Description:

Bootstrap a persistent Teleport Machine ID (tbot) setup on macOS using LaunchAgent and tbot configure identity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[webvictim](https://clawhub.ai/user/webvictim)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure engineers use this skill to set up and verify a persistent Teleport Machine ID identity on a macOS user account for agent SSH and automation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs a persistent credential-refreshing Teleport bot on a macOS user account.

Mitigation: Review before installing, use only on a trusted macOS account, and unload the LaunchAgent and remove bot state when no longer needed.

Risk: Onboarding tokens, registration secrets, generated tbot configuration, bot state, and identity outputs are sensitive.

Mitigation: Prefer secure secret delivery instead of command-line tokens or plaintext chat logs, and avoid committing generated credentials or state to source control.

Risk: The generated LaunchAgent runs a resolved tbot binary persistently and can refresh access without further prompting.

Mitigation: Verify the resolved tbot binary and generated plist before loading, then keep Teleport role scope narrow.

Risk: The bundled example uses a high bound-keypair recovery limit and includes broad illustrative Teleport-side settings.

Mitigation: Reduce recovery limits and adapt Teleport roles, labels, and policies to the minimum scope required for the deployment.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/webvictim/skills/teleport-tbot-bootstrap)
- [Teleport tbot CLI reference](https://goteleport.com/docs/reference/cli/tbot/)
- [Teleport prerequisite examples](references/teleport-prereq-examples.yaml)
- [LaunchAgent notes](references/launchagent-notes.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup steps, command proposals, validation guidance, and macOS LaunchAgent configuration for Teleport tbot identity refresh.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
