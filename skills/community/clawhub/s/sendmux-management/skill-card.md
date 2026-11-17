## Description:

Manage Sendmux domains, mailboxes, mailbox keys, sending accounts, webhooks, logs, billing, and account-level setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sendmux.ai](https://clawhub.ai/user/sendmux.ai)

### License/Terms of Use:

MIT-0

## Use Case:

Sendmux account administrators and developers use this skill to manage domains, mailboxes, sending accounts, webhooks, billing, and delivery diagnostics through authorized management connections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Management credentials or one-time secrets may be exposed.

Mitigation: Use scoped OAuth or least-privileged keys, store root keys and generated secrets securely, and never request secrets in chat.

Risk: Destructive or access-changing account actions may affect service or users.

Mitigation: Check the target and permissions, and obtain explicit confirmation before deletions, suspensions, key changes, webhook secret rotations, or provider changes.

## Reference(s):

- [Sendmux skill homepage (listed in metadata)](https://github.com/Sendmux/skills)
- [Sendmux Management on ClawHub](https://clawhub.ai/sendmux.ai/skills/sendmux-management)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown with CLI, API, and SDK examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an authorized Sendmux management connection for account operations.]

## Skill Version(s):

1.0.10 (source: ClawHub release; artifact frontmatter: 1.7.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
