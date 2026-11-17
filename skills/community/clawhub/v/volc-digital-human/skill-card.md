## Description:

Generates Volcengine digital-human talking videos from a user photo and dialog by uploading media, creating an avatar, generating TTS audio, synthesizing video, and returning the generated video assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoxiaole2025](https://clawhub.ai/user/xiaoxiaole2025)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content creators use this skill to turn a provided photo and spoken script into a Volcengine digital-human talking video with matched Chinese TTS voice. Developers can configure Volcengine credentials and run the workflow from an OpenClaw agent environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports bundled Volcengine credentials.

Mitigation: Remove bundled credentials, rotate exposed keys, and require users to provide credentials through environment variables or a local private configuration file.

Risk: The skill uploads user images and generated audio/video to public third-party file hosts.

Mitigation: Require explicit user confirmation before each upload, prefer private expiring storage, and avoid use with private photos, sensitive speech, minors' images, customer data, or regulated content.

Risk: The workflow may automatically select an inbound image and uses a shared temporary directory.

Mitigation: Require explicit image selection for each run and isolate temporary files per execution.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/xiaoxiaole2025/skills/volc-digital-human)
- [Volcengine digital human API reference](artifact/references/volc_api.md)
- [Volcengine console](https://console.volcengine.com/)
- [Volcengine access key management](https://console.volcengine.com/iam/keymanage/)
- [Volcengine visual API endpoint](https://visual.volcengineapi.com)

## Skill Output:

**Output Type(s):** [Files, Text, API Calls]

**Output Format:** [Local MP4 video and JPEG thumbnail paths with public media URLs and JSON-like workflow metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Volcengine AK/SK credentials; media is uploaded to public file hosts for API-accessible URLs, and generated video URLs may expire.]

## Skill Version(s):

1.0.4 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
