## Description:

ShellMail is a full email client for AI agents that can read inboxes, extract OTP codes, search mail, send and reply, change mailbox state, and manage a ShellMail address through the ShellMail API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaronbatchelder](https://clawhub.ai/user/aaronbatchelder)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to let an AI agent work with a dedicated ShellMail inbox for OTP retrieval, message review, sending replies, mailbox cleanup, and address lifecycle tasks. It is intended for ShellMail-specific requests, not generic email accounts or other providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A persistent SHELLMAIL_TOKEN grants full access to inbox contents, OTPs, sending, deletion, and address management.

Mitigation: Use a separate ShellMail address for agent workflows, store the token only after explicit user approval, and revoke or remove the token when access is no longer needed.

Risk: The security review reports an avoidable local command-execution risk related to numeric validation of otp --wait while the skill handles a full-access mailbox token.

Mitigation: Avoid passing untrusted wait values, review commands before execution, and consider delaying sensitive-environment use until numeric validation and token-handling fixes are available.

Risk: Delete operations can permanently remove an email or the entire ShellMail address and its mail.

Mitigation: Require explicit confirmation for the specific destructive action and verify the target email or address impact with the user before using --confirm.

## Reference(s):

- [ShellMail API](https://shellmail.ai)
- [ShellMail ClawHub Listing](https://clawhub.ai/aaronbatchelder/skills/shellmail)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and API response text or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, python3, outbound access to https://shellmail.ai, and a sensitive SHELLMAIL_TOKEN for authenticated mailbox operations.]

## Skill Version(s):

1.3.3 (source: SKILL.md frontmatter, skill.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
