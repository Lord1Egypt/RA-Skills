## Description: <br>
Download videos and get transcripts, summaries, or metadata from YouTube, TikTok, Instagram, and X (Twitter). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nogara](https://clawhub.ai/user/nogara) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill when they have a video URL and need captions, transcript text, a summary, key points, quotes, metadata, or a downloaded video file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A crafted video title could trigger unintended local shell command execution. <br>
Mitigation: Review the script before installation and avoid processing untrusted or adversarial video URLs until filename handling is fixed. <br>
Risk: Fallback transcription can upload audio content to OpenAI. <br>
Mitigation: Do not use the skill on private or sensitive videos unless this upload is acceptable; keep OPENAI_API_KEY unset or use a local transcription model when external upload is not acceptable. <br>


## Reference(s): <br>
- [Video Intelligence on ClawHub](https://clawhub.ai/nogara/video-intel) <br>
- [yt-dlp release download](https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp) <br>
- [OpenAI audio transcription API](https://api.openai.com/v1/audio/transcriptions) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text and Markdown-oriented command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create downloaded video, audio, and caption files under /tmp/video-intel by default.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
