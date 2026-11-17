## Description:

Give this agent its own email identity with Sente, including a durable sente.run address, inbox access, verification-code and magic-link handling, and workflows for registering or connecting real web accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shim2k](https://clawhub.ai/user/shim2k)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Sente when an agent needs its own email identity, must receive verification codes or magic links, or needs user-authorized durable accounts for web applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent durable access to email identities and connected accounts.

Mitigation: Install only when Sente is trusted, use a low-privilege isolated environment, authorize accounts individually, and revoke or delete accounts that are no longer needed.

Risk: Setup and account workflows can expose API keys, webhook secrets, credentials, or browser session state.

Mitigation: Use protected secret storage, avoid printing or committing secrets, prefer a pinned CLI version, and immediately delete or securely handle exported browser state.

Risk: Inbound email content may contain prompt injection or misleading instructions.

Mitigation: Treat email bodies as untrusted input and use only the extracted verification code or magic link needed for the task.

## Reference(s):

- [Sente service-integration guide](https://sente.run/skill.md)
- [Sente website and acceptable-use details](https://sente.run)
- [ClawHub skill page](https://clawhub.ai/shim2k/skills/sente)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may involve API tokens, email artifacts, browser sessions, credentials, and exported Playwright storage state.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
