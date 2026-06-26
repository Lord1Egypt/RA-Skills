## Description: <br>
Transcribes YouTube videos into timestamped transcripts and structured summaries using yt-dlp and faster-whisper. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bodysuperman](https://clawhub.ai/user/bodysuperman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, OpenClaw users, and agents use this skill to download audio from YouTube videos, transcribe speech, and return timestamped transcript text with a short structured summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Server security evidence reports that a crafted video link could cause the JavaScript launcher to run unintended commands on the user's computer. <br>
Mitigation: Fix the launcher to invoke Python with an argument array instead of shell string interpolation, and validate YouTube URLs strictly before routine use. <br>
Risk: The skill may receive video links from untrusted sources and downloads remote media before local transcription. <br>
Mitigation: Review links before execution, use the skill only in an environment approved for outbound YouTube downloads, and avoid running it with elevated privileges. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bodysuperman/youtube-transcriber-skill) <br>
- [Python downloads](https://www.python.org/downloads/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text containing progress messages followed by a Markdown-style transcript summary with timestamps.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3.8+, Node.js 14+, yt-dlp, faster-whisper, and network access to YouTube.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, skill frontmatter, package.json, and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
