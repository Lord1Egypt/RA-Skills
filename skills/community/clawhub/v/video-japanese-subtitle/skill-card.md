## Description: <br>
Automates Japanese video transcription, Simplified Chinese subtitle translation, ASS subtitle conversion, hard-subtitle rendering, and output validation for MP4 videos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xunnv](https://clawhub.ai/user/xunnv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and media workflow operators use this skill to batch-process Japanese MP4 videos into Chinese hard-subtitled outputs with resumable transcription, translation, subtitle conversion, rendering, and validation steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes an embedded QClaw gateway token. <br>
Mitigation: Rotate and replace the token before use, store credentials outside the skill source, and scope access to the minimum required translation endpoint. <br>
Risk: Video transcript text may be sent to QClaw and possibly MyMemory during translation fallback. <br>
Mitigation: Use only videos whose audio and transcripts are approved for those services, and disable or replace external fallback translation when confidentiality is required. <br>
Risk: The script contains fixed Windows input, output, and ffmpeg paths. <br>
Mitigation: Change VIDEO_DIR, OUTPUT_DIR, and FFMPEG_DIR to dedicated local folders before running the workflow. <br>
Risk: A rendered output file can pass duration checks while subtitles are missing. <br>
Mitigation: Perform frame-level visual checks as described in the skill documentation before treating the hard-subtitled video as complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xunnv/video-japanese-subtitle) <br>
- [Workflow reference](references/workflow.md) <br>
- [QClaw local chat completions endpoint](http://127.0.0.1:28789/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python configuration details, and generated subtitle/video file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces intermediate audio, SRT, translated SRT, ASS, and hard-subtitled MP4 files when the bundled script is executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
