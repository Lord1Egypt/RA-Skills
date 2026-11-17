## Description:

Composes, replies to, reply-alls, and forwards email from a Ravi email address with HTML formatting and optional attachments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raunaksingwi](https://clawhub.ai/user/raunaksingwi)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and Ravi users use this skill to compose outbound emails, reply or reply-all to existing messages, and forward threads after confirming recipients and message content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Accidental outbound email may be sent to the wrong recipients or with unintended subject, body, quoted thread content, or attachments.

Mitigation: Verify recipients, subject, body, quoted thread content, and attachment-related details before compose, reply-all, forward, or attachment-related use.

Risk: Email content or user input may be handled unsafely if used to construct shell-evaluated command strings.

Mitigation: Pass Ravi CLI arguments safely as arguments rather than building shell-evaluated command strings from email content or user input.

## Reference(s):

- [Ravi Messages API schema](https://ravi.id/docs/schema/messages.json)
- [Ravi Attachments API schema](https://ravi.id/docs/schema/attachments.json)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Ravi CLI command patterns, HTML email body guidance, recipient resolution guidance, and rate-limit handling notes.]

## Skill Version(s):

2.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
