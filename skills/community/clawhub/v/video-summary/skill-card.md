## Description:

Video summarization for Bilibili, Xiaohongshu, Douyin, and YouTube. Extract insights from video content through transcription and summarization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lifei68801](https://clawhub.ai/user/lifei68801)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to extract transcripts from online videos or local media and produce structured summary requests, summaries, chapter breakdowns, timestamps, or raw subtitles for agent-assisted review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private videos, meeting recordings, or account-restricted content may expose sensitive transcript data.

Mitigation: Process only authorized content, review outputs before sharing, and avoid shared systems for sensitive media.

Risk: Cookie files may contain session tokens and can be used by yt-dlp when accessing supported platforms.

Mitigation: Use cookies only when necessary, use cookies from accounts you control, and keep cookie files private.

Risk: Sensitive transcript data may remain in unsafe temporary paths until temporary-file handling is fixed.

Mitigation: Run the skill in an isolated workspace or private machine and remove temporary transcript or media files after use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lifei68801/skills/video-summary)
- [Publisher Profile](https://clawhub.ai/user/lifei68801)
- [yt-dlp Documentation](https://github.com/yt-dlp/yt-dlp)
- [OpenAI Whisper](https://github.com/openai/whisper)
- [OpenAI API Keys](https://platform.openai.com/api-keys)
- [Zhipu GLM](https://open.bigmodel.cn/)
- [DeepSeek Platform](https://platform.deepseek.com/)
- [Moonshot Platform](https://platform.moonshot.cn/)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text, Markdown, or JSON summary output with optional transcript-only output and structured summary requests.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires yt-dlp, jq, ffmpeg, ffprobe, and bc. Whisper, LLM API credentials, custom API endpoints, and cookies are optional depending on the source media and summarization workflow.]

## Skill Version(s):

1.6.4 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
