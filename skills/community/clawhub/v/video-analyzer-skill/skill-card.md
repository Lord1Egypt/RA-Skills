## Description: <br>
Video Analyzer downloads, transcribes, and analyzes videos from YouTube, X/Twitter, and TikTok using local Whisper processing to produce transcripts, summaries, timestamps, and actionable insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[minilozio](https://clawhub.ai/user/minilozio) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, developers, and agents use this skill to inspect video URLs, produce timestamped transcripts, summarize key moments, answer content questions, or save video/audio locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports that the script can build unsafe shell commands from user-provided values, which could let a crafted request run unintended local commands. <br>
Mitigation: Review before installing or use only with trusted video URLs and simple language codes, and review proposed commands before execution. <br>
Risk: The skill may contact video sites, download Whisper models, create temporary transcripts, and save requested media to the user's Desktop. <br>
Mitigation: Run it only where those network, storage, and Desktop writes are expected, and remove generated files when they are no longer needed. <br>


## Reference(s): <br>
- [Video Analyzer ClawHub Page](https://clawhub.ai/minilozio/video-analyzer-skill) <br>
- [Video Analyzer Homepage](https://github.com/minilozio/video-analyzer-skill) <br>
- [whisper.cpp Model Downloads](https://huggingface.co/ggerganov/whisper.cpp/resolve/main/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown summaries, timestamped transcript text, local media files, and shell command invocations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create temporary transcript files, download Whisper models when needed, and save requested media files to the user's Desktop.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
