## Description: <br>
Generates Tencent Cloud VOD command-line workflows for media upload, pull upload, search, semantic search, media processing, image processing, AIGC image/video/chat operations, token management, sub-application lookup, task lookup, and knowledge-base import. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tencent-mpaas-skills](https://clawhub.ai/user/tencent-mpaas-skills) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to produce precise Python commands for Tencent Cloud VOD uploads, media queries, transformations, AIGC generation, and related administrative tasks. It is intended for agent-assisted command generation where users provide the required media identifiers, URLs, files, prompts, or task identifiers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Tencent Cloud credentials and can read or write dotenv-based credential configuration. <br>
Mitigation: Use scoped Tencent Cloud credentials, keep dotenv files private, avoid shared environments, and rotate credentials if exposure is suspected. <br>
Risk: Media processing and AIGC operations can create Tencent Cloud charges. <br>
Mitigation: Review exact commands before execution, prefer dry-run for uncertain or high-cost work, and configure budget alerts or spending limits in Tencent Cloud. <br>
Risk: Runtime auto-upgrade behavior can change the local Python environment. <br>
Mitigation: Review the auto-upgrade helper before use and run the skill in an isolated environment rather than a shared or production Python installation. <br>
Risk: Media URLs, prompts, session context, and retained task data may contain sensitive information. <br>
Mitigation: Submit only data approved for Tencent Cloud processing and clear local task or generated records according to the user's data-retention requirements. <br>


## Reference(s): <br>
- [Tencent Cloud VOD pricing](https://cloud.tencent.com/document/product/266/2838) <br>
- [Tencent Cloud budget center](https://console.cloud.tencent.com/expense/budget) <br>
- [vod_upload detailed parameters and examples](artifact/references/vod_upload.md) <br>
- [vod_pull_upload detailed parameters and examples](artifact/references/vod_pull_upload.md) <br>
- [vod_describe_media detailed parameters and examples](artifact/references/vod_describe_media.md) <br>
- [vod_process_media detailed parameters and examples](artifact/references/vod_process_media.md) <br>
- [vod_process_image detailed parameters and examples](artifact/references/vod_process_image.md) <br>
- [vod_aigc_chat detailed parameters and examples](artifact/references/vod_aigc_chat.md) <br>
- [vod_aigc_image detailed parameters and examples](artifact/references/vod_aigc_image.md) <br>
- [vod_aigc_video detailed parameters and examples](artifact/references/vod_aigc_video.md) <br>
- [vod_aigc_token detailed parameters and examples](artifact/references/vod_aigc_token.md) <br>
- [vod_search_media detailed parameters and examples](artifact/references/vod_search_media.md) <br>
- [vod_search_media_by_semantics detailed parameters and examples](artifact/references/vod_search_media_by_semantics.md) <br>
- [vod_import_media_knowledge detailed parameters and examples](artifact/references/vod_import_media_knowledge.md) <br>
- [vod_describe_task detailed parameters and examples](artifact/references/vod_describe_task.md) <br>
- [vod_describe_sub_app_ids detailed parameters and examples](artifact/references/vod_describe_sub_app_ids.md) <br>
- [vod_scene_aigc_image detailed parameters and examples](artifact/references/vod_scene_aigc_image.md) <br>
- [vod_create_scene_aigc_video_task detailed parameters and examples](artifact/references/vod_create_scene_aigc_video_task.md) <br>
- [vod_create_aigc_advanced_custom_element detailed parameters and examples](artifact/references/vod_create_aigc_advanced_custom_element.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration guidance] <br>
**Output Format:** [Markdown text containing exact Python shell commands and Markdown links for returned media URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands are expected to use scripts/ paths, observe documented required parameters, and use dry-run or explicit confirmation for uncertain or high-cost processing operations.] <br>

## Skill Version(s): <br>
1.0.9 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
