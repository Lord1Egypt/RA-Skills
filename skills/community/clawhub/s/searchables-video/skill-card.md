## Description:

YouTube, Bilibili, and local video search, analysis, Q&A, summarization, highlights, and article generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dejavukong](https://clawhub.ai/user/dejavukong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to search a Searchables video library, inspect YouTube, Bilibili, and local video content, and generate summaries, Q&A answers, highlights, articles, subtitles, and Notion exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can search a private video library and send sensitive queries or file paths to a configured API endpoint.

Mitigation: Use it only with a trusted Searchables desktop app, pin the endpoint to the expected local or trusted origin, and confirm before searching private videos or processing local files.

Risk: Browser-cookie-backed video access and Notion export can expose private or account-linked content.

Mitigation: Require explicit user confirmation before using private video access or exporting content to Notion, and review selected export modules before sending data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dejavukong/skills/searchables-video)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, Configuration guidance]

**Output Format:** [Markdown or plain text with curl commands, JSON API examples, citations, summaries, articles, and export guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call a configured Searchables API endpoint, may include video timestamps and source citations, and may initiate long-running processing only after user confirmation.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
