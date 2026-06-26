## Description: <br>
Clips YouTube videos locally with yt-dlp and ffmpeg, supporting highlight selection, translation, CapCut-style karaoke subtitles, and an optional Groq Whisper transcription fallback when YouTube subtitles are unavailable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chyyynh](https://clawhub.ai/user/chyyynh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and video editors use this skill to create local clips from YouTube videos, select highlight segments, translate subtitles, and burn bilingual karaoke-style captions into the result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional Groq transcription fallback can send downloaded audio to a third-party transcription API. <br>
Mitigation: Leave GROQ_API_KEY unset, or decline the fallback, when audio is private, sensitive, copyrighted, or should stay local. <br>
Risk: YouTube cookies may be requested for throttled or restricted downloads. <br>
Mitigation: Provide cookies only when necessary, preferably through a temporary limited cookie file. <br>
Risk: The skill asks the agent to run yt-dlp, ffmpeg, and Python commands that download and process media locally. <br>
Mitigation: Review generated commands before execution and run them in a trusted local workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chyyynh/video-clip-skill) <br>
- [Groq audio transcription API endpoint](https://api.groq.com/openai/v1/audio/transcriptions) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and Python snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local command guidance for yt-dlp, ffmpeg, Python subtitle processing, optional Groq transcription calls, and generated subtitle or video files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
