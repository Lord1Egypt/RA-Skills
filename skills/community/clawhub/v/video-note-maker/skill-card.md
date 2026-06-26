## Description: <br>
提取视频音频，分段转写生成详细笔记和整理版，并可发送处理完成通知。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fang232629](https://clawhub.ai/user/fang232629) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students and knowledge workers use this skill to turn local educational videos into transcripts and Markdown study notes. It is aimed at Chinese-language video workflows using ffmpeg and Whisper, with optional email or Feishu progress notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically email local video filenames, paths, output paths, and file sizes. <br>
Mitigation: Use it only on videos whose filenames and paths are acceptable to share by email, and avoid auto mode until the outbound email behavior is reviewed. <br>
Risk: Generated notes may include content that does not accurately reflect the input video. <br>
Mitigation: Verify generated notes against the transcript before using them for study, publication, or decision-making. <br>
Risk: Helper monitor scripts include hard-coded local paths and process-killing behavior. <br>
Mitigation: Do not run monitor helper scripts unless the hard-coded paths and process management behavior are acceptable in the target environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fang232629/video-note-maker) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown notes, transcript text files, and shell command invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes temporary audio and transcript files plus final Markdown notes; may send email or Feishu notifications when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
