## Description:

将外语长视频转成中文字幕成片，并切成多条带钩子标题、封面和封面帧的 9:16 竖屏短片，可选择发布到微信视频号、抖音、小红书和公众号。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dizhu](https://clawhub.ai/user/dizhu)

### License/Terms of Use:

MIT

## Use Case:

External creators, operators, and developers use this skill to repurpose long foreign-language videos into Chinese-subtitled long-form outputs, vertical short clips, cover images, and optional social-platform publishing batches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use browser automation and social-account session files for public posting.

Mitigation: Use dedicated browser profiles and social accounts, start with one test post, and publish only in small batches with spacing between posts.

Risk: The workflow may use API credentials for external image generation.

Mitigation: Keep credentials scoped to environment variables, prefer the intended Ofox key path, and avoid the OPENROUTER_API_KEY fallback unless it has been reviewed.

Risk: Setup installs or clones media and publishing dependencies that affect local execution.

Mitigation: Review or pin dependencies before setup and install only in an environment intended for this workflow.

Risk: Some media-processing steps modify generated files in place.

Mitigation: Keep backups of source media and intermediate outputs before running batch processing or cover-prepending steps.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dizhu/skills/video-viral-pipeline)
- [social-auto-upload dependency](https://github.com/dreammis/social-auto-upload.git)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands and JSON configuration examples; generated artifacts include MP4 video clips and JPG/PNG cover images.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local media files and optional API credentials or social-account session files.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
