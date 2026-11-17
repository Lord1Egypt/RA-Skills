## Description:

Quick upload video to AIOZ Stream API. Create video objects with default or custom encoding configurations, upload the file, complete the upload, then return the video link to the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vinhbui3004](https://clawhub.ai/user/vinhbui3004)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to create AIOZ Stream video objects, upload local video files, finalize uploads, and retrieve streaming links. It also supports custom encoding settings, thumbnail upload, and transcoding cost checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable AIOZ Stream credentials are required for API calls.

Mitigation: Use least-privileged or short-lived upload keys where possible, and avoid passing secrets on the command line.

Risk: The skill sends credentials and media files to a hard-coded service endpoint.

Mitigation: Verify that `api-w3stream.attoaioz.cyou` is the intended endpoint for the account before installing or running the skill.

Risk: The artifact includes account-changing video operations beyond the upload flow.

Mitigation: Allow delete, update, thumbnail, or cost-related operations only when the user explicitly requests them.

Risk: Local media paths identify files that may be uploaded to the service.

Mitigation: Confirm the exact file path and intended visibility before upload.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vinhbui3004/skills/video-upload-aioz-stream)
- [AIOZ Stream API endpoint](https://api-w3stream.attoaioz.cyou)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and md5sum; API keys and local media paths are provided by the user.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
