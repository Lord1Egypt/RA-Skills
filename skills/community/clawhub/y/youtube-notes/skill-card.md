## Description:

Convert YouTube videos into clean, structured markdown notes with steps, tools, timestamps, and parts lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[welbinator](https://clawhub.ai/user/welbinator)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn YouTube tutorials, repair videos, how-to videos, and educational videos into structured reference notes without rewatching the video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for a TranscriptAPI.com API key, and the security review notes that pasting keys into chat can expose credentials.

Mitigation: Configure TRANSCRIPT_API_KEY through a protected secret manager or environment setting instead of sharing the key in chat.

Risk: Video URLs or IDs may be sent to TranscriptAPI.com and YouTube.

Mitigation: Avoid private, unlisted, or sensitive video links unless that disclosure is acceptable.

## Reference(s):

- [TranscriptAPI](https://transcriptapi.com)
- [ClawHub Skill Page](https://clawhub.ai/welbinator/skills/youtube-notes)

## Skill Output:

**Output Type(s):** [Markdown, Text, Guidance]

**Output Format:** [Structured Markdown notes with headings, lists, source links, and timestamp links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TRANSCRIPT_API_KEY and may use YouTube video metadata and descriptions as source material.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
