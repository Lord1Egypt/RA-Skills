## Description: <br>
特看视频 lets an agent generate and edit videos, images, digital avatars, voiceovers, cloned voices, backgrounds, product model images, and board-organized media workflows from natural-language requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wxjhhhh](https://clawhub.ai/user/wxjhhhh) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
External creators, marketers, educators, and developers use this skill to ask an agent for AI-generated media assets and multi-step creative production workflows. The skill is suited for creating videos, images, avatars, voiceovers, cloned voices, product visuals, and organized board results through Tekan/TopView service scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores Tekan/TopView credentials locally after browser authorization. <br>
Mitigation: Install only when the user accepts local credential storage; use the provided logout flow or remove saved credentials when access is no longer needed. <br>
Risk: Selected images, audio, and video files can be uploaded to an external AI media service. <br>
Mitigation: Avoid uploading sensitive files and confirm that the user intends to send the selected media to Tekan/TopView before generation. <br>
Risk: Voice cloning and face or avatar generation can affect consent, likeness, and impersonation expectations. <br>
Mitigation: Get clear consent before using a person's face or voice, and avoid workflows that impersonate people without authorization. <br>
Risk: Board and custom voice deletion commands can remove user-managed assets. <br>
Mitigation: Verify board IDs, task IDs, and voice IDs with the user before deleting boards or cloned voices. <br>
Risk: Webhook URLs may send task-completion data to destinations outside the user's control. <br>
Mitigation: Use webhook URLs only when the destination is trusted and needed for the workflow. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wxjhhhh/tekan) <br>
- [Publisher Profile](https://clawhub.ai/user/wxjhhhh) <br>
- [Tekan Video](https://video.tekan.cn) <br>
- [README](README.md) <br>
- [Auth Module](references/auth.md) <br>
- [Video Generation Module](references/video_gen.md) <br>
- [AI Image Module](references/ai_image.md) <br>
- [Avatar4 Module](references/avatar4.md) <br>
- [Product Avatar Module](references/product_avatar.md) <br>
- [Remove Background Module](references/remove_bg.md) <br>
- [Text2Voice Module](references/text2voice.md) <br>
- [Voice Module](references/voice.md) <br>
- [Board Module](references/board.md) <br>
- [User Module](references/user.md) <br>
- [Model Mapping](references/model_mapping.md) <br>
- [Error Handling Guide](references/error_handling.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands and service-generated media URLs or downloaded files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include links to Tekan boards for viewing, editing, and downloading generated results.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
