## Description:

Tencent VOD helps agents generate precise Python commands for Tencent Cloud VOD uploads, media processing, media search, AIGC tasks, token management, and task queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tencent-mpaas-skills](https://clawhub.ai/user/tencent-mpaas-skills)

### License/Terms of Use:

MIT License

## Use Case:

Developers and operators use this skill to turn Tencent Cloud VOD requests into executable Python commands for uploading media, processing video and images, querying assets and tasks, managing AIGC tokens, and launching AIGC media workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary says the skill can modify the active Python environment during dependency setup.

Mitigation: Install and run it in a dedicated virtual environment, and inspect dependency and pip configuration before first use.

Risk: The release security guidance says Tencent VOD AIGC tokens may be stored in plaintext dotenv files.

Mitigation: Keep dotenv files out of source control, restrict file permissions, and revoke or rotate any token that appears in logs or shared files.

Risk: The skill can generate commands for billable Tencent Cloud VOD media processing and AIGC services.

Mitigation: Use dry-run previews and explicit confirmation for processing or high-cost tasks, and configure Tencent Cloud expense alerts or spending limits.

## Reference(s):

- [Tencent VOD on ClawHub](https://clawhub.ai/tencent-mpaas-skills/skills/tencent-vod)
- [Tencent Cloud VOD Pricing](https://cloud.tencent.com/document/product/266/2838)
- [Tencent Cloud VOD Upload API](https://cloud.tencent.com/document/api/266/31766)
- [Tencent Cloud VOD Pull Upload API](https://cloud.tencent.com/document/api/266/35575)
- [Tencent Cloud VOD Process Media API](https://cloud.tencent.com/document/api/266/33431)
- [Tencent Cloud VOD AIGC Image API](https://cloud.tencent.com/document/api/266/126240)
- [Tencent Cloud VOD AIGC Video API](https://cloud.tencent.com/document/api/266/126239)
- [Tencent Cloud VOD AIGC Token API](https://cloud.tencent.com/document/api/266/128054)
- [vod_upload reference](references/vod_upload.md)
- [vod_pull_upload reference](references/vod_pull_upload.md)
- [vod_describe_media reference](references/vod_describe_media.md)
- [vod_search_media reference](references/vod_search_media.md)
- [vod_search_media_by_semantics reference](references/vod_search_media_by_semantics.md)
- [vod_process_media reference](references/vod_process_media.md)
- [vod_describe_task reference](references/vod_describe_task.md)
- [vod_aigc_chat reference](references/vod_aigc_chat.md)
- [vod_aigc_token reference](references/vod_aigc_token.md)
- [vod_aigc_image reference](references/vod_aigc_image.md)
- [vod_aigc_video reference](references/vod_aigc_video.md)
- [vod_aigc_audio reference](references/vod_aigc_audio.md)
- [vod_process_image reference](references/vod_process_image.md)
- [vod_scene_aigc_image reference](references/vod_scene_aigc_image.md)
- [vod_create_scene_aigc_video_task reference](references/vod_create_scene_aigc_video_task.md)
- [vod_import_media_knowledge reference](references/vod_import_media_knowledge.md)
- [vod_describe_sub_app_ids reference](references/vod_describe_sub_app_ids.md)
- [vod_create_aigc_advanced_custom_element reference](references/vod_create_aigc_advanced_custom_element.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text commands with Markdown links for returned URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands target Python scripts under scripts/ and may include dry-run flags, confirmation guidance, and environment setup guidance.]

## Skill Version(s):

1.1.3 (source: server-resolved release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
