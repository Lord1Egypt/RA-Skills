## Description: <br>
Generate AI videos through SkillBoss API Hub from text prompts, first-frame or first-and-last-frame images, reference images, and supported Seedance model options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate, download, inspect, and optionally share AI-generated video assets from prompts or source images. It is intended for workflows that need configurable video duration, resolution, aspect ratio, audio generation, and Seedance model hints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper may send SKILLBOSS_API_KEY to an API domain that differs from the documented base URL. <br>
Mitigation: Verify the expected API domain before use and use a limited, revocable API key. <br>
Risk: Prompts, images, generated videos, and optional Feishu transfers are handled by external services. <br>
Mitigation: Avoid confidential media or prompts and treat Feishu delivery as external file sharing. <br>
Risk: The macOS download flow uses a shell-based opener for saved files. <br>
Mitigation: Avoid untrusted or metacharacter-containing download paths until that opener is replaced. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tobeyrebecca/toby-video-generation) <br>
- [SkillBoss Pilot API Endpoint](https://api.skillbossai.com/v1/pilot) <br>
- [CLI API Endpoint Observed in Artifact](https://api.heybossai.com/v1/pilot) <br>
- [Feishu Video Sharing Guide](artifact/how_to_send_video_via_feishu_app.md) <br>
- [Feishu Media Upload API](https://open.feishu.cn/open-apis/drive/v1/medias/upload_all) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash, Python CLI, curl, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce external video URLs and downloaded MP4 files when the API call succeeds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
