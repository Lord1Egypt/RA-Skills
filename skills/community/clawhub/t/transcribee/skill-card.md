## Description: <br>
Transcribee transcribes YouTube, Instagram Reels, TikTok, and local audio/video files with speaker diarization into clean transcripts for LLM analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[itsfabioroma](https://clawhub.ai/user/itsfabioroma) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
External users and developers use this skill to transcribe online or local media, produce speaker-labeled transcript files, and organize the results into a local transcript library for later LLM analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Media and transcript content is sent to cloud transcription and categorization services. <br>
Mitigation: Use only with media that is acceptable to send to ElevenLabs and Anthropic, and avoid sensitive local recordings unless the provider processing terms are acceptable. <br>
Risk: AI-generated categorization influences where transcript files are written. <br>
Mitigation: Review generated categories and constrain transcript output to the intended local transcript directory before relying on saved files. <br>
Risk: Required API keys and privacy expectations are not fully disclosed by server evidence. <br>
Mitigation: Confirm required ElevenLabs and Anthropic credentials and add clear privacy disclosure before installing or using the skill. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/itsfabioroma/transcribee) <br>
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) <br>
- [FFmpeg](https://ffmpeg.org/) <br>
- [ElevenLabs](https://elevenlabs.io/) <br>
- [Anthropic](https://anthropic.com/) <br>
- [Clawdbot](https://github.com/clawdbot/clawdbot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands, Configuration guidance] <br>
**Output Format:** [Speaker-labeled transcript text files and JSON metadata written to a local transcripts folder.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional raw JSON includes word-level timing data; output folders are organized by an AI-generated category and media title.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence; package.json reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
