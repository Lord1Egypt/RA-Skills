## Description: <br>
自然语言媒体助手，用于视频压缩、MP4/MOV 封面提取、音频转换和字幕识别。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[370299455cx-web](https://clawhub.ai/user/370299455cx-web) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and media workflow operators use this skill to run local or HTTP media-processing jobs from natural-language requests or structured JSON pipelines. It supports compression, thumbnail extraction, audio extraction, ASR/OCR subtitle generation, caption segmentation, batch work, and persisted asynchronous jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The unauthenticated local HTTP service can fetch remote URLs and write output files in the workspace. <br>
Mitigation: Keep the service bound to 127.0.0.1, avoid exposing it on 0.0.0.0 without authentication, and install it only when this local media-processing server is needed. <br>
Risk: The skill can read approved local media paths and stores persisted job details and output paths. <br>
Mitigation: Limit media_roots to intended directories and avoid passing sensitive file paths or prompts. <br>
Risk: Media-processing actions may overwrite generated outputs. <br>
Mitigation: Use overwrite=false when preserving existing outputs matters. <br>
Risk: Runtime behavior depends on media-processing and ML dependencies. <br>
Mitigation: Review, pin, and update dependencies before use, and verify ffmpeg, ffprobe, ASR, and OCR dependencies in the deployment environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/370299455cx-web/skills/ym-mediatoolkit) <br>
- [Maintenance guide](artifact/MAINTENANCE.md) <br>
- [Skill interface metadata](artifact/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [JSON responses, Markdown guidance, shell commands, configuration snippets, and generated media or caption files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Media outputs are written under workspace output directories; HTTP jobs persist status, results, and output paths for polling.] <br>

## Skill Version(s): <br>
4.2.2 (source: server release metadata; artifact frontmatter and skill.json report 4.3.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
