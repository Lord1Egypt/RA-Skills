## Description:

Send batch SMS messages to up to 100 domestic or international phone numbers through the CloudSMS API with custom content and an optional signature.

This skill is ready for commercial/non-commercial use.

## Publisher:

[picccabo-art](https://clawhub.ai/user/picccabo-art)

### License/Terms of Use:

MIT-0

## Use Case:

Operations, support, and developer users can use this skill through an agent to send transactional or notification SMS messages with CloudSMS credentials. It is suited to workflows that need bulk delivery status and concise troubleshooting guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles CloudSMS Auth Key credentials directly.

Mitigation: Use a protected secret source for the Auth Key and avoid exposing credentials in prompts, logs, or shell history.

Risk: The skill can send billable SMS messages.

Mitigation: Ask for explicit user confirmation before sending and verify recipients, message content, and expected cost-sensitive scope.

Risk: The documentation states recipient and content limits that should be enforced before delivery.

Mitigation: Validate that each request stays within the 100-recipient and 500-character limits before invoking the CloudSMS API.

Risk: The helper clears HTTP proxy environment variables before making the request.

Mitigation: Review network routing requirements before installation and avoid silent proxy bypass in managed environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/picccabo-art/skills/sms-sender)
- [CloudSMS API endpoint](https://cpaas-sms.cmidict.com:1820/uips)

## Skill Output:

**Output Type(s):** [text, shell commands, API calls, guidance]

**Output Format:** [JSON script result summarized as human-facing text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May make billable CloudSMS SMS_SEND_REQUEST calls using user-provided Channel ID and Auth Key.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
