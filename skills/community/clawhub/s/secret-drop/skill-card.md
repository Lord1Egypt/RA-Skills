## Description:

Password/API key in Telegram/Discord/Slack or OpenClaw-masked: request pwpush/snappwd link, ingest it, or share stored secrets as one-time link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sprintberlin](https://clawhub.ai/user/sprintberlin)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to move API keys, passwords, and similar secrets into or out of OpenClaw messenger workflows through short-lived one-time links without printing plaintext in chat, logs, or command output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read local secrets and upload them to a third-party one-time-link service when asked.

Mitigation: Install it only where chat users are trusted operators or where outbound share requests are controlled by approval and source restrictions.

Risk: Outbound sharing may expose production credentials through provider-hosted one-time links.

Mitigation: Prefer self-hosted or organization-approved providers, restrict which files or secret names agents may export, and avoid outbound production credential sharing without a separate approval process.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sprintberlin/skills/secret-drop)
- [Password Pusher](https://pwpush.com)
- [SnapPwd](https://snappwd.io)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and secret-free JSON status checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should avoid plaintext secrets and return only confirmations, metadata, or one-time URLs.]

## Skill Version(s):

0.2.0 (source: pyproject.toml and CHANGELOG, released 2026-09-19)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
