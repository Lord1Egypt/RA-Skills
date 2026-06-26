## Description: <br>
Downloads TikTok, Instagram Reel, X/Twitter video, YouTube Short, and other social video links with yt-dlp, with an optional transcript workflow for creating reusable skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[olliewazza](https://clawhub.ai/user/olliewazza) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to download social video links in best available quality and, when needed, produce a transcript and source material for creating a concise OpenClaw skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Transcription mode may upload extracted audio to OpenAI when OPENAI_API_KEY is set. <br>
Mitigation: Run without OPENAI_API_KEY for local-only download and extraction, or require an explicit confirmation before cloud transcription. <br>
Risk: The skill can download media from third-party social platforms. <br>
Mitigation: Use it only for videos the user is allowed to download and ask before using logged-in browser sessions or cookies. <br>


## Reference(s): <br>
- [ClawHub release: Social Downloader](https://clawhub.ai/olliewazza/social-downloader) <br>
- [OpenAI audio transcription API](https://api.openai.com/v1/audio/transcriptions) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Markdown, Code, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and local file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce downloaded video files, extracted audio, result JSON, transcript text, and guidance for creating or updating an OpenClaw skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
