## Description:

Vidu helps agents use vwu.ai video-generation models for text-to-video and image-to-video workflows through shell commands that create, poll, and download generation tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a3273283](https://clawhub.ai/user/a3273283)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to configure a VWU API key, submit Vidu video prompts, optionally include a reference image, check task status, and download generated MP4 files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, selected images, and the VWU API key may be sent to the configured API service.

Mitigation: Use only the intended HTTPS vwu.ai endpoint, avoid submitting sensitive prompts or images, and leave VWU_BASE_URL unset unless a trusted endpoint is required.

Risk: Persistent plaintext storage of VWU_API_KEY in shell startup files can expose the token.

Mitigation: Prefer a session-scoped environment variable or a local secret manager, and rotate the token if it may have been exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/a3273283/skills/vwu-vidu)
- [vwu.ai console](https://vwu.ai)
- [Vidu image-to-video documentation](https://platform.vidu.cn/docs/image-to-video)
- [New API documentation](https://docs.newapi.ai/en)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with inline shell commands and command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce task identifiers, status messages, and downloaded MP4 files when the shell commands are executed.]

## Skill Version(s):

1.1.0 (source: server release metadata and artifact changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
