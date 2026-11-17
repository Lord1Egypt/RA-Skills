## Description:

Use the Sendmux CLI for durable agent inbox registration, owner invites, profiles, and terminal-driven Management, Mailbox, and Sending workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sendmux.ai](https://clawhub.ai/user/sendmux.ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to set up Sendmux inboxes and profiles, check access, and carry out email, mailbox, and account-management tasks from a terminal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials for mailbox, sending, or account management could be exposed or granted excessive access.

Mitigation: Keep keys in a secret store or environment and use scoped profiles or OAuth where possible; do not paste secrets into chat or command arguments.

Risk: Sending mail or changing account settings can have unintended effects.

Mitigation: Review send and account-management commands before execution and confirm destructive actions explicitly.

Risk: Saved profiles can retain access after the task ends.

Mitigation: Log out or revoke profiles when access is no longer needed.

## Reference(s):

- [Sendmux CLI skill on ClawHub](https://clawhub.ai/sendmux.ai/skills/sendmux-cli)
- [Sendmux skills homepage](https://github.com/Sendmux/skills)
- [Sendmux OAuth for REST APIs](https://sendmux.ai/docs/developer-tools/oauth)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI responses can be requested as machine-readable JSON.]

## Skill Version(s):

1.0.12 (source: ClawHub release; artifact frontmatter: 1.7.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
