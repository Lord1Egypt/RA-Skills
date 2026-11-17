## Description:

Sends a financial-market daily report email with generated summary text and Word or PowerPoint attachments, including RFC 2231 filename encoding for Chinese attachments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[szrw1825](https://clawhub.ai/user/szrw1825)

### License/Terms of Use:

MIT-0

## Use Case:

Employees or agents preparing daily financial-market reports use this skill to send a generated market summary with Word and PowerPoint attachments to a configured recipient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes an SMTP authorization code in its documentation.

Mitigation: Rotate the exposed credential and remove secrets from documentation before installing or executing the skill.

Risk: The script relies on an unreviewed external Python config module before sending local attachments.

Mitigation: Replace the executable config import with a reviewed non-executable configuration source and require explicit preview of recipient, subject, body, and attachments before sending.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/szrw1825/skills/send-email-to)
- [ClawHub publisher profile](https://clawhub.ai/user/szrw1825)

## Skill Output:

**Output Type(s):** [Text, Shell commands]

**Output Format:** [Plain text logs and an email message sent with optional document attachments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses configured market-data and attachment paths; sends one email to the configured recipient.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
