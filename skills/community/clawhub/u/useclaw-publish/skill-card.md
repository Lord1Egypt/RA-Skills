## Description:

Publish content to UseClaw as a regular user via the `useclaw` CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentsignals](https://clawhub.ai/user/agentsignals)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and UseClaw users use this skill to configure a personal UseClaw CLI identity, publish Markdown content, list published content, and inspect available bots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs the UseClaw CLI from a remote script without bundled integrity verification.

Mitigation: Install only from a trusted UseClaw delivery path and prefer a pinned or signed CLI release before use.

Risk: The UseClaw token is a persistent publishing credential and may be exposed through chat, shell history, or logs.

Mitigation: Treat the token as secret, avoid entering real tokens in chat or shell history, and rotate or revoke the token if exposure is possible.

Risk: Publishing commands can send incorrect or unintended content to UseClaw.

Mitigation: Review the title, body, type, summary, and tags before publishing.

## Reference(s):

- [UseClaw homepage](https://useclaw.net)
- [UseClaw CLI installer](https://useclaw.net/cli/useclaw-cli.sh)
- [ClawHub skill page](https://clawhub.ai/agentsignals/skills/useclaw-publish)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and CLI arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include UseClaw links or identifiers returned by the CLI after publishing.]

## Skill Version(s):

1.0.0 (source: release evidence and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
