## Description:

Sends video notifications to specified mobile phone numbers through an IVVR platform service, using an existing server-side video file path with a maximum file size of 5 MB.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhu-xiao-di](https://clawhub.ai/user/zhu-xiao-di)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to trigger single-recipient or batch video notifications from a configured IVVR notification service. It is intended for workflows where the video file already exists on the server and the recipient phone numbers are supplied by the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send phone notifications through the configured service.

Mitigation: Require clear user confirmation before sending notifications and restrict use to authorized recipient lists.

Risk: API keys, recipient phone numbers, and server file paths may be sent to the configured endpoint, including over plaintext HTTP if misconfigured.

Mitigation: Use only trusted HTTPS endpoints, avoid public plaintext ngrok URLs, scope and rotate API keys, and treat phone numbers and file paths as sensitive data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhu-xiao-di/skills/video-notification)
- [Publisher profile](https://clawhub.ai/user/zhu-xiao-di)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON service response with success status, file ID, and message fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured API endpoint, API key, server-side video file path, and one or more recipient phone numbers.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
