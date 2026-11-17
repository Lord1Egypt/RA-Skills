## Description:

Generates Python commands for Tencent Cloud VOD upload, media processing, querying, AIGC image, video, audio, chat, token, search, image-processing, sub-application, and task-status workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tencent-mpaas-skills](https://clawhub.ai/user/tencent-mpaas-skills)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to turn Tencent Cloud VOD tasks into concrete Python script commands. It supports media upload, processing, metadata lookup, AIGC generation and chat, token and usage management, semantic search, image processing, sub-application discovery, and asynchronous task tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can submit billable Tencent Cloud VOD, media-processing, and AIGC tasks.

Mitigation: Use dry-run previews and require explicit confirmation before processing, AIGC, batch, or other high-cost commands; configure Tencent Cloud budget alerts and caps.

Risk: The skill uses Tencent Cloud credentials and AIGC tokens, and token operations may expose sensitive values in logs or shared terminals.

Mitigation: Run in a dedicated virtual environment with least-privilege credentials, keep secrets in a secure secret manager or private environment file, avoid logging token commands, and rotate exposed tokens.

Risk: The security verdict is suspicious because dependencies may be installed or upgraded automatically and long-lived cloud tokens may be stored in local files or output.

Mitigation: Review or disable the auto-upgrade helper before execution, pin and review dependencies, and scan the skill before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tencent-mpaas-skills/skills/tencent-vod-intl)
- [vod_upload](references/vod_upload.md)
- [vod_pull_upload](references/vod_pull_upload.md)
- [vod_describe_media](references/vod_describe_media.md)
- [vod_search_media](references/vod_search_media.md)
- [vod_search_media_by_semantics](references/vod_search_media_by_semantics.md)
- [vod_process_media](references/vod_process_media.md)
- [vod_process_image](references/vod_process_image.md)
- [vod_describe_task](references/vod_describe_task.md)
- [vod_describe_sub_app_ids](references/vod_describe_sub_app_ids.md)
- [vod_aigc_chat](references/vod_aigc_chat.md)
- [vod_aigc_token](references/vod_aigc_token.md)
- [vod_aigc_image](references/vod_aigc_image.md)
- [vod_aigc_video](references/vod_aigc_video.md)
- [vod_aigc_audio](references/vod_aigc_audio.md)
- [vod_scene_aigc_image](references/vod_scene_aigc_image.md)
- [vod_create_scene_aigc_video_task](references/vod_create_scene_aigc_video_task.md)
- [vod_create_aigc_advanced_custom_element](references/vod_create_aigc_advanced_custom_element.md)
- [vod_import_media_knowledge](references/vod_import_media_knowledge.md)
- [Tencent Cloud VOD pricing](https://cloud.tencent.com/document/product/266/2838)
- [Tencent Cloud billing center](https://console.cloud.tencent.com/expense)
- [Tencent Cloud VOD API reference](https://cloud.tencent.com/document/product/266)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Code, Configuration guidance]

**Output Format:** [Markdown or plain text containing Python shell commands and Markdown links for generated media URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands target scripts under scripts/ and may include dry-run, no-wait, JSON-output, polling, and Tencent Cloud environment configuration options.]

## Skill Version(s):

1.1.3 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
