## Description: <br>
Converts video or audio files from URLs into text transcripts or SRT subtitles using speech recognition APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SxLiuYu](https://clawhub.ai/user/SxLiuYu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to transcribe supported video or audio URLs into plain text or subtitle output for review, reuse, or accessibility workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports a command-injection flaw in the tool wrapper that could allow crafted input to run shell commands on the host. <br>
Mitigation: Do not install in a normal environment until the wrapper is fixed; evaluate only in a sandbox with trusted media URLs. <br>
Risk: The skill downloads media locally and uploads it to external transcription services, which can expose private recordings or confidential audio. <br>
Mitigation: Avoid private recordings, signed URLs, and confidential business audio unless the external service and data handling are approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SxLiuYu/video-transcribe-pro) <br>
- [Publisher profile](https://clawhub.ai/user/SxLiuYu) <br>
- [MyShell transcription endpoint](https://api.myshell.ai/v1/audio/transcriptions) <br>
- [OpenAI audio transcription endpoint](https://api.openai.com/v1/audio/transcriptions) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text transcript or SRT subtitle text returned through the agent tool response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts a media URL, optional language code, and output format; artifact documentation states a 25 MB file size limit.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
