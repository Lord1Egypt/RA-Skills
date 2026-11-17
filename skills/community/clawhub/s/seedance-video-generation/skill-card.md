## Description:

Generate AI videos using ByteDance Seedance from text prompts, first-frame or first-and-last-frame images, reference images, and task-management requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackycser](https://clawhub.ai/user/jackycser)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and agent users use this skill to create, poll, download, and manage Seedance video-generation tasks through the Volcengine Ark API. It supports text-to-video, image-to-video, draft workflows, and optional Feishu sharing guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, image files, image URLs, generated videos, and optional Feishu-shared files may be sent to external service providers.

Mitigation: Avoid sensitive or private media unless the user has approved the data transfer and the provider terms are acceptable.

Risk: The macOS download auto-open path can run unintended shell commands.

Mitigation: Avoid the --download auto-open workflow on macOS until the shell call is replaced with a non-shell subprocess call and task IDs and paths are validated.

Risk: Feishu sharing can distribute generated videos beyond the local workspace.

Mitigation: Require explicit user approval before Feishu sharing and confirm the target channel, recipient, and file path.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jackycser/skills/seedance-video-generation)
- [Volcengine Ark API Base URL](https://ark.cn-beijing.volces.com/api/v3)
- [Feishu Media Upload API](https://open.feishu.cn/open-apis/drive/v1/medias/upload_all)
- [Feishu Message Send API](https://open.feishu.cn/open-apis/im/v1/messages/send)
- [Feishu Video Sending Guide](how_to_send_video_via_feishu_app.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python CLI and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce task IDs, status JSON, video URLs, downloaded MP4 files, and Feishu sharing guidance.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
