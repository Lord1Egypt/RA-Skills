## Description: <br>
Generates and edits short videos with Volcengine Doubao Seedance models, including text-to-video, image-to-video, and audio-enabled video workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiujiahong](https://clawhub.ai/user/qiujiahong) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to turn text prompts, images, reference images, and optional audio settings into short generated videos through Doubao Seedance, then save or share the resulting MP4 output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, images, and generated videos are sent to third-party services. <br>
Mitigation: Use only with content approved for Volcengine and any configured sharing service. <br>
Risk: The API base URL configuration is mishandled in the artifact. <br>
Mitigation: Patch and verify VIDEO_GEN_BASE_URL handling before running the generator. <br>
Risk: Volcengine and Feishu credentials are required for the documented workflows. <br>
Mitigation: Store credentials in secure environment or secret storage and avoid embedding them in prompts, files, or logs. <br>
Risk: The artifact includes Feishu upload and message-send guidance for generated videos. <br>
Mitigation: Require explicit user confirmation before uploading or sending videos to Feishu. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qiujiahong/video-gen) <br>
- [Doubao Seedance API Reference](references/api.md) <br>
- [Volcengine Ark Console](https://console.volcengine.com/ark) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with shell commands, Python snippets, MP4 file paths, and optional task JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May download generated MP4 files or return task JSON when no-wait mode is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
