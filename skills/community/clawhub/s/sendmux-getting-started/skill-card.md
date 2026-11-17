## Description:

Set up Sendmux for agents, register a durable inbox without an existing key, link an owner, choose a runtime surface, and make the first harmless call.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sendmux.ai](https://clawhub.ai/user/sendmux.ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect an agent to Sendmux, choose the appropriate credential and interface, optionally register an inbox, and verify access without sending a message.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unverified package sources could introduce unwanted code during installation.

Mitigation: Verify the Sendmux package sources before installing.

Risk: Broad credentials or exposed API keys can grant unnecessary access.

Mitigation: Use least-privileged keys or OAuth scopes, and store secrets in environment variables or a secret manager rather than chat or logs.

Risk: A self-registered agent profile retains durable inbox read access until revoked.

Mitigation: Understand the profile's access lifetime and revoke the registration when access is no longer needed.

## Reference(s):

- [Sendmux skill on ClawHub](https://clawhub.ai/sendmux.ai/skills/sendmux-getting-started)
- [Sendmux skills homepage](https://github.com/Sendmux/skills)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown with shell and TypeScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes mailbox, management, and sending tasks to the appropriate surface; connection checks do not send email.]

## Skill Version(s):

1.0.10 (ClawHub release; embedded skill version: 1.7.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
