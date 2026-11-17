## Description:

Short Video Parser extracts metadata from short-video and image-gallery share links across major platforms and can transcribe video speech into text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangbuyiya](https://clawhub.ai/user/yangbuyiya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to parse shared short-video URLs into structured metadata and to convert video speech into text for content review, notes, subtitles, or summarization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: URL parsing and media handling can make unintended network requests.

Mitigation: Use trusted video links, prefer the local parser, and run the skill with restricted network egress where possible.

Risk: Downloaded video and extracted audio files are retained by default.

Mitigation: Set auto_cleanup_temp_files=true or pass --auto_cleanup true unless retained media files are explicitly needed.

Risk: Supplying untrusted parsed-result JSON can bypass normal parsing assumptions.

Mitigation: Avoid untrusted --parse_result input and review parsed metadata before using it in downstream workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangbuyiya/skills/yby6-video-parser-skill)
- [SiliconFlow audio transcription API documentation](https://docs.siliconflow.cn/api-reference/audio)
- [SiliconFlow](https://siliconflow.cn/)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [JSON parsing results, transcription text, and Markdown transcription reports with command-line and environment configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transcription can write Markdown reports under demos/ and temporary video or audio files under tmp/.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
