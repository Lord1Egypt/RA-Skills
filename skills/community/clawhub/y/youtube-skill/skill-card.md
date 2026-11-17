## Description:

YouTube skill: get a finished video found on YouTube, then upload it. Transcribes it (free local faster-whisper, your own Groq or OpenAI key, or an existing SRT/VTT), finds the phrases people actually type into YouTube search (free autocomplete, optional free YouTube Data API key), writes 10 titles, a description whose first lines work in search, chapters, tags and hashtags, checks every field against YouTube's limits, renders thumbnail options from the video's own frames and previews them at feed size, writes clean captions, then uploads to YouTube with WoopSocial after you say yes, plus a YouTube Studio checklist. Works on Mac, Windows and Linux with ffmpeg and Pillow; no paid API required. Use when someone says "upload to youtube," "youtube seo," "youtube title," "youtube description," "youtube tags," "youtube chapters," "youtube thumbnail," "publish my video," or "youtube with Claude Code." Never promises what the video doesn't deliver, confirms before anything posts. Standalone: needs no other skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[social-media-skills](https://clawhub.ai/user/social-media-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and channel managers use the skill to prepare and publish YouTube videos with search-aware titles, descriptions, chapters, tags, captions, and thumbnails, then review post performance. It supports a human approval step before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports that a video may transfer to WoopSocial and its Cloudflare storage before publication approval, and that a conditional path could upload an unintended local file.

Mitigation: Require explicit approval before any video transfer, separately from approval to publish, and verify the selected local video before upload.

Risk: Cloud transcription can use a curl fallback that needs safer handling of text fields and language codes.

Mitigation: Before cloud transcription, fix the fallback to treat text fields literally and validate language codes; for private media, explicitly choose local transcription or existing captions.

Risk: Connection credentials could be exposed if API keys are placed in connection URLs.

Mitigation: Prefer OAuth over API keys in connection URLs.

## Reference(s):

- [YouTube SEO guidance](artifact/references/youtube-seo.md)
- [WoopSocial upload and posting guidance](artifact/references/woopsocial.md)
- [YouTube Skill on ClawHub](https://clawhub.ai/social-media-skills/skills/youtube-skill)
- [YouTube Search](https://www.youtube.com/howyoutubeworks/product-features/search/)
- [WoopSocial MCP tools reference](https://docs.woopsocial.com/mcp/tools-reference)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown, JSON, plain text, and command-line instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates video metadata, captions, thumbnail previews, and a YouTube Studio checklist from the supplied video and user choices.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
