## Description: <br>
Use when the user wants to repurpose a YouTube video for Bilibili, add bilingual English-Chinese subtitles to a video, or create hardcoded subtitle versions for Chinese platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agents365-ai](https://clawhub.ai/user/agents365-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to turn YouTube videos or playlists into Bilibili-ready MP4s with bilingual subtitles and Chinese publish metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The default download workflow can use a logged-in Chrome YouTube session for cookie-backed downloads. <br>
Mitigation: Prefer public downloads without cookies, use a separate low-privilege browser profile or scoped cookie file when cookies are needed, and require confirmation before cookie-backed download or playlist processing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agents365-ai/yt2bb) <br>
- [ffmpeg documentation](https://ffmpeg.org/) <br>
- [yt-dlp documentation](https://github.com/yt-dlp/yt-dlp) <br>
- [OpenAI Whisper](https://github.com/openai/whisper) <br>
- [Aegisub subtitle editor](https://aegisub.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with shell commands and generated media/subtitle files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces MP4, SRT, ASS, and publish_info.md outputs; utility commands can emit JSON for agent-friendly validation.] <br>

## Skill Version(s): <br>
2.5.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
