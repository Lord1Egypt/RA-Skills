## Description:

Helps agents inspect video links, retrieve available metadata, and summarize key information from supported platforms such as YouTube and Bilibili.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackeven02](https://clawhub.ai/user/jackeven02)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to ask an agent what a linked video is about and to extract available titles, descriptions, durations, chapters, subtitles, key points, and viewing priorities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may fetch video metadata from third-party platforms or use tools such as yt-dlp, which can expose requests to platform policies and external services.

Mitigation: Use vetted tools in an isolated environment, avoid exposing secrets, and fetch or download media only where rights and platform terms allow it.

Risk: Summaries can be incomplete when subtitles, chapters, descriptions, or platform APIs are unavailable, and the artifact states the skill cannot directly understand video frames.

Mitigation: Treat results as metadata-based analysis unless transcript or API content is available, and disclose source limitations in user-facing summaries.

## Reference(s):

- [Video Understanding reference resources](artifact/references/resources.md)
- [ClawHub skill page](https://clawhub.ai/jackeven02/skills/video-learn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown text with optional shell command examples and API call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries depend on metadata, descriptions, chapters, subtitles, or API responses available from the source platform; the skill does not directly play video or analyze raw visual frames.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
