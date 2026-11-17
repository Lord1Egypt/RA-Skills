## Description:

Sends an IVVR video notification to a specified mobile phone number using a local video file path and phone number.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhu-xiao-di](https://clawhub.ai/user/zhu-xiao-di)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to upload a local video file up to 5 MB to a configured IVVR service and send a video notification call to a specified 11-digit mobile number.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: TLS certificate verification is disabled while sending videos, phone numbers, and authentication headers.

Mitigation: Require HTTPS, remove verify=False, and verify certificates before production use.

Risk: A misconfigured or untrusted BASE_URL could receive media, phone numbers, and service credentials.

Mitigation: Restrict BASE_URL to approved IVVR hosts and use credentials dedicated to this service.

Risk: The workflow handles phone numbers and video content that may be sensitive.

Mitigation: Use only non-sensitive videos and phone numbers unless appropriate consent, policy review, and operational controls are in place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhu-xiao-di/skills/video-notification-pro)
- [ClawHub publisher profile](https://clawhub.ai/user/zhu-xiao-di)

## Skill Output:

**Output Type(s):** [JSON, API Calls]

**Output Format:** [JSON object with success status, message, file_id, and task_id fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates an external IVVR notification as a side effect when the configured service accepts the upload and send requests.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
