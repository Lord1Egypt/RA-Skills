## Description:

Send emails through the Resend API when a user wants to send an email, deliver a report by email, forward generated content to an inbox, or trigger an email notification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chjm-ai](https://clawhub.ai/user/chjm-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to send formatted HTML email, deliver generated reports or summaries, and trigger lightweight notifications through a configured Resend account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent can send user-provided content through the user's Resend account.

Mitigation: Review the recipient, subject, and body before sending, especially when the message contains sensitive content.

Risk: The skill depends on local Resend credentials and sender configuration.

Mitigation: Keep the local .env file private, trusted, and unwritable by other users or processes.

## Reference(s):

- [README](README.md)
- [Save To Email ClawHub Page](https://clawhub.ai/chjm-ai/skills/save-to-email)
- [Resend Email API Endpoint](https://api.resend.com/emails)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command examples and environment configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires RESEND_API_KEY, RESEND_FROM, curl, and python3; sends one HTML email per command invocation.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
