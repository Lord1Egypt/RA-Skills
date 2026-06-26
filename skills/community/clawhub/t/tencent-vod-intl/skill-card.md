## Description: <br>
Tencent Cloud VOD command generation assistant for upload, media processing, media query, AIGC image/video/chat/token workflows, search, image processing, sub-application queries, and task status commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tencent-mpaas-skills](https://clawhub.ai/user/tencent-mpaas-skills) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and media operations teams use this skill to generate Tencent Cloud VOD Python commands for uploads, processing jobs, AIGC workflows, media search, metadata queries, and task tracking. It is intended for users who already operate Tencent Cloud VOD resources and can review potentially billable commands before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can submit billable Tencent Cloud VOD and AIGC operations. <br>
Mitigation: Review each generated command before execution, use --dry-run for uncertain or high-cost jobs, and configure billing alerts or caps. <br>
Risk: The skill requires Tencent Cloud credentials and may handle AIGC tokens. <br>
Mitigation: Store only the required Tencent Cloud variables in the dotenv files used by the skill and avoid placing unrelated secrets there. <br>
Risk: Inputs may include private media URLs or signed links. <br>
Mitigation: Avoid pasting private or signed URLs unless approved for the current workflow. <br>
Risk: The release includes behavior that can automatically change the local Python environment and persist token or task metadata. <br>
Mitigation: Review or disable runtime auto-upgrade and automatic token persistence before use in controlled environments. <br>


## Reference(s): <br>
- [Tencent VOD Intl. on ClawHub](https://clawhub.ai/tencent-mpaas-skills/tencent-vod-intl) <br>
- [VOD Upload](references/vod_upload.md) <br>
- [VOD Pull Upload](references/vod_pull_upload.md) <br>
- [VOD Process Media](references/vod_process_media.md) <br>
- [VOD Describe Media](references/vod_describe_media.md) <br>
- [VOD Describe Task](references/vod_describe_task.md) <br>
- [VOD Search Media](references/vod_search_media.md) <br>
- [VOD Semantic Search](references/vod_search_media_by_semantics.md) <br>
- [VOD AIGC Chat](references/vod_aigc_chat.md) <br>
- [VOD AIGC Image](references/vod_aigc_image.md) <br>
- [VOD AIGC Video](references/vod_aigc_video.md) <br>
- [VOD AIGC Token](references/vod_aigc_token.md) <br>
- [VOD Process Image](references/vod_process_image.md) <br>
- [VOD Scene AIGC Image](references/vod_scene_aigc_image.md) <br>
- [VOD Scene AIGC Video Task](references/vod_create_scene_aigc_video_task.md) <br>
- [VOD Import Media Knowledge](references/vod_import_media_knowledge.md) <br>
- [VOD Custom Element](references/vod_create_aigc_advanced_custom_element.md) <br>
- [Tencent Cloud VOD Pricing](https://cloud.tencent.com/document/product/266/2838) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown with Tencent Cloud VOD Python commands and links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands are expected to use the scripts/ path prefix, support dry-run review, and may require Tencent Cloud environment variables.] <br>

## Skill Version(s): <br>
1.0.9 (source: SKILL.md metadata and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
