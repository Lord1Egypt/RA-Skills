## Description:

Generate AI videos using ByteDance Seedance from text prompts, first-frame images, first-and-last-frame image pairs, or reference images, and manage asynchronous video generation tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asikochen](https://clawhub.ai/user/asikochen)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and creative operators use this skill to create short AI-generated videos through the Volcengine Ark API, download completed videos, and optionally share generated video files through Feishu workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, images, generated videos, and task metadata may be sent to Volcengine, and Feishu sharing may send video files to Feishu.

Mitigation: Avoid sensitive personal or proprietary content unless the destination services and account policies are approved for that data.

Risk: The Feishu sharing guide includes a concrete recipient identifier and external upload flow.

Mitigation: Replace recipient IDs with verified destinations and confirm Feishu permissions, file-size limits, and rate limits before sharing.

Risk: The CLI opens downloaded videos on macOS through a shell command, which evidence.security flags as a local shell-execution risk for crafted or untrusted paths.

Mitigation: Use trusted download paths only, or replace shell-based opening with a non-shell subprocess call before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/asikochen/skills/seedance-video-creation)
- [Volcengine Ark API endpoint](https://ark.cn-beijing.volces.com/api/v3)
- [Feishu media upload API](https://open.feishu.cn/open-apis/drive/v1/medias/upload_all)
- [Feishu message send API](https://open.feishu.cn/open-apis/im/v1/messages/send)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with Python and shell command examples, JSON API responses, and downloaded MP4 video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ARK_API_KEY; may transmit prompts, images, generated videos, and task metadata to external services.]

## Skill Version(s):

1.0.0 (source: target metadata, release evidence, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
