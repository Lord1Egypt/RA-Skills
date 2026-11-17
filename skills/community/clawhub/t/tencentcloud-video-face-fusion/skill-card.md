## Description:

Uses Tencent Cloud Video Creation APIs to submit and query video face-fusion jobs that merge provided face images into template videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neck-cn](https://clawhub.ai/user/neck-cn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to automate Tencent Cloud video face-fusion workflows, including task submission, polling, and result lookup for template videos and user-provided face images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send face images and video material to Tencent Cloud under the user's credentials.

Mitigation: Use only with explicit consent for all faces and videos, and confirm the Tencent Cloud account and service terms before execution.

Risk: Local paths supplied as face images may be read and uploaded as base64 media.

Mitigation: Avoid untrusted local paths and run the skill in a restricted environment with access only to intended media files.

Risk: The scripts can auto-install an unpinned Tencent SDK package at runtime.

Mitigation: Preinstall a pinned `tencentcloud-sdk-python` version in the execution environment before using the skill.

Risk: Generated videos can omit the AI-generated label when configured to do so.

Mitigation: Keep the AI-generated label enabled unless there is a legitimate reason to disable it.

## Reference(s):

- [Submit Video Face Fusion Job API](references/submit_video_face_fusion_api.md)
- [Describe Video Face Fusion Job API](references/describe_video_face_fusion_api.md)
- [Tencent Cloud Video Creation Console](https://console.cloud.tencent.com/vclm)
- [Tencent Cloud API Key Management](https://console.cloud.tencent.com/cam/capi)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown instructions with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include Tencent Cloud job IDs, task status, error details, and result video URLs.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
