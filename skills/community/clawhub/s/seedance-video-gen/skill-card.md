## Description:

Generates AI videos with ByteDance Seedance models through the Volcengine Ark API, supporting text-to-video, image-to-video, first/last frame generation, reference images, and asynchronous task status management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lovensky1992-wk](https://clawhub.ai/user/lovensky1992-wk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and OpenClaw users use this skill to ask an agent to create, poll, download, list, or delete Seedance video generation tasks from text prompts or image inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and image inputs may be sent to Volcengine/ByteDance during video generation.

Mitigation: Use only non-sensitive prompts and images that the user is authorized to upload.

Risk: Credential handling can expose ARK_API_KEY if commands or environment checks are displayed carelessly.

Mitigation: Do not print API keys or include secrets in logs, prompts, screenshots, or shared output.

Risk: The security scan reports a macOS auto-open command-injection bug in download-path handling.

Mitigation: Avoid macOS auto-open behavior and choose simple trusted download paths until the bug is fixed.

Risk: Delete actions are destructive and can cancel or remove the wrong task.

Mitigation: Confirm the exact task ID and user intent before running delete operations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lovensky1992-wk/skills/seedance-video-gen)
- [Publisher Profile](https://clawhub.ai/user/lovensky1992-wk)
- [Seedance curl API reference](references/curl-api-reference.md)
- [Volcengine Console](https://console.volcengine.com/)
- [Volcengine Ark API base URL](https://ark.cn-beijing.volces.com/api/v3)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, CLI usage, JSON API responses, task IDs, and downloaded video file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce API requests to Volcengine Ark, upload local images as data URLs, poll asynchronous tasks, download MP4 files, and perform destructive delete actions when requested.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
