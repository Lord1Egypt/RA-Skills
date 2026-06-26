## Description: <br>
Video Transcriber is a workflow for Bilibili and YouTube videos that retrieves existing subtitles or downloads audio and transcribes it with Whisper when subtitles are unavailable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xing2xian](https://clawhub.ai/user/xing2xian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and end users can use this skill to summarize video content, retrieve captions, or transcribe Bilibili and YouTube videos in Chinese or English. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Example download commands weaken connection security by using --no-check-certificate. <br>
Mitigation: Prefer removing --no-check-certificate and use the workflow only with trusted Bilibili or YouTube links. <br>
Risk: The workflow can create temporary local audio and transcript files. <br>
Mitigation: Run it in a workspace where temporary media files are acceptable and can be reviewed or deleted after use. <br>
Risk: The workflow depends on local tools and a referenced watcher extension. <br>
Mitigation: Install only when those dependencies are expected and acceptable for the target agent environment. <br>


## Reference(s): <br>
- [Artifact Skill Definition](artifact/SKILL.md) <br>
- [ClawHub Release Page](https://clawhub.ai/xing2xian/video-transcriber) <br>
- [Publisher Profile](https://clawhub.ai/user/xing2xian) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and transcript or summary text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or reference local temporary audio and transcript files during transcription workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
