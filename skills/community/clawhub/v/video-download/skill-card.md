## Description: <br>
Download videos from 1800+ websites and generate subtitles using Faster Whisper AI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[upupc](https://clawhub.ai/user/upupc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, creators, and external users use this skill to download videos from supported sites, extract audio, and produce transcripts or subtitle files for authorized content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated downloads can expose or use sensitive browser and session cookies. <br>
Mitigation: Use cookie, cookiesfrombrowser, or cookiefile options only for trusted workflows, owned accounts, and confirmed target URLs; avoid pasting raw cookies when an exported scoped cookie file is sufficient. <br>
Risk: Subtitle-only requests can unexpectedly fall back to full video download and transcription when subtitle download fails. <br>
Mitigation: Confirm storage and network expectations before running subtitle-only mode, monitor the output directory, and stop the run if full media download is not intended. <br>
Risk: The skill can write large video, audio, transcript, and model-related files locally. <br>
Mitigation: Choose an explicit output directory with enough disk space and review generated files before reusing or sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/upupc/video-download) <br>
- [Project homepage](https://github.com/upupc/video-download) <br>
- [yt-dlp supported extractors](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md) <br>
- [Supported sites reference](references/supportedsites.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Text, Configuration instructions] <br>
**Output Format:** [Downloaded media and audio files plus subtitle or transcript files in TXT, SRT, VTT, or JSON formats.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python and ffmpeg; transcription can download and run a Faster Whisper model.] <br>

## Skill Version(s): <br>
0.1.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
