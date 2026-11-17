## Description:

青萍 AI 图片生成工具，通过青萍 AI API 生成图片并自动下载到本地，支持多种模型、尺寸和比例配置，默认生成 16:9 比例图片。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lusyoe](https://clawhub.ai/user/lusyoe)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to submit prompts to Qingping AI, poll for completion, and download generated PNG images for creative or design workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts are sent to Qingping's external API.

Mitigation: Use prompts appropriate for external processing and review data-sharing requirements before use.

Risk: The remote API can control downloaded URLs and filenames, which may write outside the advertised folder.

Mitigation: Run the skill in a limited workspace where unintended PNG writes or large downloads would not damage important files.

Risk: The Qingping API key can authorize external service use.

Mitigation: Use a limited, rotatable API key and avoid committing shell profile files or other files containing the key.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lusyoe/skills/qingping-ai-skill)
- [Qingping AI platform profile and API key page](https://auth.lusyoe.com/profile)
- [Qingping image generation API](https://video.lusyoe.com/api/img/generations)
- [Qingping image generation status API](https://video.lusyoe.com/api/img/generations/{task_id}/status)

## Skill Output:

**Output Type(s):** [files, shell commands, configuration, guidance]

**Output Format:** [Downloaded PNG image files with console status text and command-line usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires QINGPING_API_KEY and writes generated images to the qingping-ai directory.]

## Skill Version(s):

1.0.4 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
