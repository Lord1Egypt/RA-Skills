## Description:

Automatically fetch YouTube video subtitles and generate concise summaries for key points, talks, and long videos across supported subtitle languages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[potatosolo](https://clawhub.ai/user/potatosolo)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, researchers, and learners use this skill to extract captions from public YouTube videos and turn long-form video content into concise notes, executive summaries, key points, and optional detailed summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: YouTube captions are untrusted source text and may contain prompt-injection attempts or misleading content.

Mitigation: Treat captions only as material to summarize, not as instructions to follow, and avoid exposing unrelated secrets, tools, or conversation history during summarization.

Risk: The skill depends on a third-party transcript package to fetch public captions.

Mitigation: Pin and review dependency versions before installation or deployment.

Risk: The skill is intended for public videos with captions and may fail or produce incomplete summaries when captions are unavailable.

Mitigation: Use it only for public videos with available captions and verify important summaries against the original video when accuracy matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/potatosolo/skills/youtube-video-summary)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown summaries, plain text subtitle formatting, and optional Python or shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summary length can be short, medium, or detailed when requested; output may include video title, source link, executive summary, key points, and detailed notes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
