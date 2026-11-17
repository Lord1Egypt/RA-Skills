## Description: <br>
视频帧提取-免费版帮助代理使用本地 ffmpeg 从视频文件提取首帧、指定时间点单帧或最多 10 张缩略图。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content creators use this skill to ask an agent to extract local video frames for covers, previews, social posts, and study notes. It is intended for simple local frame capture and thumbnail generation rather than batch media production or editing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The trigger language is broader than the documented free-edition capability and could be selected for unrelated audio editing, media conversion, dubbing, network callback, or bulk media workflows. <br>
Mitigation: Use this skill only for local video frame or thumbnail extraction, and route unsupported media editing or conversion requests to a more appropriate reviewed skill. <br>
Risk: The skill relies on local ffmpeg command execution against user-provided video paths and output locations. <br>
Mitigation: Confirm the input file and output path before execution, avoid untrusted shell interpolation, and review generated commands before running them. <br>
Risk: The artifact states that copyright-protected media processing is outside the intended use. <br>
Mitigation: Use the skill only with media the user is authorized to process. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/video-frames-tool-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and local output file paths for JPG or PNG frame images] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local ffmpeg; the free edition is described as handling one video per run and up to 10 generated thumbnails.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
