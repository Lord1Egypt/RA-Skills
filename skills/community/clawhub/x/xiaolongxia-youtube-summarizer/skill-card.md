## Description:

Summarizes YouTube videos by gathering video metadata, transcripts, and related web coverage into structured Chinese or English summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whsml22](https://clawhub.ai/user/whsml22)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to turn a YouTube link into a structured summary for events, technical talks, or news videos. The summary can include video details, core points, supporting links, and language-matched output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes web requests to YouTube and search or news providers based on the video the user provides.

Mitigation: Use it only with video links and search terms that are appropriate to disclose to those services.

Risk: The artifact describes optional memory recording and EvoMap publication paths that could retain or share generated summaries.

Mitigation: Allow saving to memory files or preparing EvoMap publication only when the user explicitly wants the content retained or shared.

Risk: Generated summaries may be incomplete when a video is unavailable, private, deleted, or lacks sufficient transcript and search evidence.

Mitigation: State source limitations in the summary and rely on available video metadata, transcript content, and corroborating coverage.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/whsml22/skills/xiaolongxia-youtube-summarizer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summaries with tables, lists, source links, and optional inline shell commands; the helper script can emit JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Matches the user's language and may include video metadata, transcript-derived content, citations, and timestamped transcript text when available.]

## Skill Version(s):

1.1.0 (source: server release metadata and SKILL.md footer)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
