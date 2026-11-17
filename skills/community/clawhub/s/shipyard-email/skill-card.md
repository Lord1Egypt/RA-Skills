## Description:

Helps set up email on a custom domain, configure SPF, DKIM, and DMARC, test deliverability, and send owner notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[philipposk](https://clawhub.ai/user/philipposk)

### License/Terms of Use:

MIT-0

## Use Case:

App developers use this skill to set up custom-domain email in Gmail, check mail authentication and deliverability, and send deployment or other owner notices through the Shipyard plugin. The full plugin is required for its scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release artifact does not include the executable Shipyard scripts, so their behavior was unavailable for review.

Mitigation: Review the full Shipyard plugin and its scripts before installing.

Risk: Diagnostic email results can be viewed by anyone with the exact mail-tester test address.

Mitigation: Use dummy content for diagnostic emails.

Risk: Sharing credentials in chat or files could expose mail access.

Mitigation: Keep keys out of chat and files; enter the sending-only key directly in Gmail as directed.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/philipposk/skills/shipyard-email)
- [Email on your own domain](references/email-domain.md)
- [Owner email notifications](references/notify.md)
- [Mail-tester FAQ](https://mail-tester.com/faq)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Shell commands, Text]

**Output Format:** [Markdown with DNS record examples and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the full Shipyard plugin's scripts; the user completes DNS and provider setup steps.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
