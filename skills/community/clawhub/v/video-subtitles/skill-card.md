## Description: <br>
Generate SRT subtitles from video/audio with translation support. Transcribes Hebrew (ivrit.ai) and English (whisper), translates between languages, burns subtitles into video. Use for creating captions, transcripts, or hardcoded subtitles for WhatsApp/social media. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ngutman](https://clawhub.ai/user/ngutman) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, creators, and media teams use this skill to transcribe Hebrew or English audio/video, generate SRT subtitles, translate Hebrew subtitles to English, and create hardcoded subtitle videos for sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Processing sensitive media or writing subtitle and video outputs can expose private content if run in an untrusted local environment. <br>
Mitigation: Run the skill only in a trusted environment, review output locations, and avoid sensitive videos unless local processing and model downloads are acceptable. <br>
Risk: Subtitle embedding and burn-in operations run ffmpeg on media files provided by the user. <br>
Mitigation: Use media files from trusted sources and inspect generated output paths before relying on the results. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/ngutman/video-subtitles) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Shell commands, Guidance] <br>
**Output Format:** [Plain text transcripts, SRT subtitle files, and MP4 video files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May download speech models on first use and can invoke ffmpeg to embed or burn subtitles when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
