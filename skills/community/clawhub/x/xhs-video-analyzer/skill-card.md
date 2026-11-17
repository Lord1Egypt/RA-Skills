## Description:

Downloads Xiaohongshu videos, extracts audio, sends audio chunks to Poe/Gemini for transcription, and helps an agent produce a detailed Chinese content summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hviktortsoi](https://clawhub.ai/user/hviktortsoi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to process a Xiaohongshu video URL into a local video, extracted audio, transcript, and structured Chinese analysis summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The downloader can fetch arbitrary non-Xiaohongshu URLs.

Mitigation: Use only with intended Xiaohongshu URLs, avoid elevated privileges, and prefer a private trusted working directory until URL validation is tightened.

Risk: Video audio is sent to Poe/Gemini for transcription and video, audio, chunks, and transcript files are stored locally.

Mitigation: Use the skill only when the user is comfortable uploading the video's audio to Poe/Gemini and storing derived files locally; remove local artifacts when no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hviktortsoi/skills/xhs-video-analyzer)
- [Poe API endpoint used for transcription](https://api.poe.com/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown analysis summary plus transcript text and local media/transcript files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates video.mp4, audio.mp3, audio.txt, and chunked audio files in a local working directory.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
