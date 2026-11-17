## Description:

Helps users choose an audience, draft and test a Sendly email campaign, and send it after confirming the recipient count.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devino](https://clawhub.ai/user/devino)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams and other Sendly users can draft campaigns for existing contacts, review the audience and message, send a test, and explicitly approve a final send.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A campaign could reach unintended recipients or send unreviewed content.

Mitigation: Review the audience count, subject, and sender address; require explicit approval of the stated recipient count before sending.

Risk: A sender address may not belong to a verified sending domain.

Mitigation: Check domain verification before creating the campaign and stop if the sender domain is not verified.

## Reference(s):

- [Sending Email Campaigns on ClawHub](https://clawhub.ai/devino/skills/sendly-sending-email-campaigns)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Campaign subject and body, audience count, draft status, and test or send result.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
