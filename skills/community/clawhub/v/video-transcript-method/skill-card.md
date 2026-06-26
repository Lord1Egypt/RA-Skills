## Description: <br>
Video Transcript Method helps agents extract structured transcripts from online videos by checking available subtitles first, falling back to Whisper speech recognition, and organizing results with timestamps, metadata, chapters, and key points. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and content workers use this skill to turn user-provided online videos into structured transcript artifacts. It guides subtitle detection, audio extraction, speech-to-text transcription, semantic segmentation, and summary formatting while preserving user review of the final transcript. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may fetch user-provided video URLs, download media or subtitle files, and write transcript files locally. <br>
Mitigation: Use a deliberate output directory and process only videos that are appropriate for the user's copyright, privacy, and data-handling obligations. <br>
Risk: The workflow includes SSL verification bypass guidance for troubleshooting downloads. <br>
Mitigation: Keep SSL verification enabled during normal use and avoid disabling it unless absolutely necessary. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangjiaocheng/video-transcript-method) <br>
- [Publisher profile](https://clawhub.ai/user/wangjiaocheng) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown or text transcript files with timestamps, metadata, chapter sections, key-point tables, and optional shell commands for subtitle, audio, and transcription steps.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local transcript files and may use yt-dlp and Whisper when subtitles are unavailable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
