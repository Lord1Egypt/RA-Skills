## Description:

Generate AI videos from text prompts or images through SkillBoss API Hub, with support for Seedance 1.5 Pro, 1.0 Pro, 1.0 Pro Fast, and 1.0 Lite model hints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers, creators, and external users use this skill to generate short AI videos from text prompts, first-frame or first-and-last-frame images, and reference images, then optionally download or share the result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends SKILLBOSS_API_KEY credentials, prompts, and user media to an external API domain.

Mitigation: Verify that api.heybossai.com is the intended and trusted recipient before use, and avoid submitting sensitive prompts or images.

Risk: The Feishu sharing guide includes a fixed recipient identifier.

Mitigation: Replace the recipient with the intended chat or user before using the sharing flow.

Risk: Downloaded videos may be auto-opened on macOS through a shell call.

Mitigation: Fix or disable the macOS auto-open behavior before running downloads in managed environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobeyrebecca/skills/toby-video-generation)
- [Publisher profile](https://clawhub.ai/user/tobeyrebecca)
- [Feishu video sharing guide](artifact/how_to_send_video_via_feishu_app.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python CLI and shell command examples; the CLI prints JSON metadata and can download MP4 video files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and sends prompts, media inputs, and generation requests to an external API endpoint.]

## Skill Version(s):

1.0.0 (source: target metadata and SKILL.md frontmatter; CHANGELOG top entry is v1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
