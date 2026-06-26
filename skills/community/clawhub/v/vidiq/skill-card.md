## Description: <br>
AI-powered video intelligence - download, analyze, clip, GIF from any URL. Supports YouTube, TikTok, Instagram, X. Uses ffmpeg + yt-dlp. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cassh100k](https://clawhub.ai/user/cassh100k) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect, download, sample, clip, convert, and summarize videos from supported URLs or local files. It supports AI video analysis workflows by extracting frames that can be sent to a vision model for content understanding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports that the tool evaluates video metadata as code while processing arbitrary media. <br>
Mitigation: Review before installing and prefer a fixed version that replaces eval-based frame-rate parsing with safe fraction parsing. <br>
Risk: Downloaded videos, extracted frames, audio, clips, and mosaics are cached under /tmp/vidiq. <br>
Mitigation: Use only media you are allowed to download or process and clear /tmp/vidiq after handling sensitive or private videos on shared systems. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cassh100k/vidiq) <br>
- [Publisher profile](https://clawhub.ai/user/cassh100k) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, guidance] <br>
**Output Format:** [Markdown with inline bash commands and generated media file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ffmpeg and yt-dlp. Outputs may include video metadata, extracted frames, clips, GIFs, MP3 audio, scene-change timestamps, mosaics, and cached files under /tmp/vidiq.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
