## Description:

Fetch public TikTok videos by keyword, creator, or comment thread and return structured JSON for topic research, competitor monitoring, creator screening, and comment analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guaikei](https://clawhub.ai/user/guaikei)

### License/Terms of Use:

MIT

## Use Case:

Content creators, marketers, and analysts use this skill to research public TikTok videos and comments, identify topic and engagement patterns, monitor competitor posts, and screen creators.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and TikTok URLs are sent to Guaikei's API, and requests require an API token.

Mitigation: Use queries and public profile or video links that are appropriate to share with the service, and keep GUAIKEI_API_TOKEN out of prompts and shared logs.

Risk: The security scan has medium confidence because some scripts were only partially inspected.

Mitigation: Review the skill source before installing or enabling it.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/guaikei/skills/tt-topic-hunter)
- [Guaikei TikTok data API](https://www.guaikei.com)
- [FAQ and environment setup](artifact/references/faq.md)
- [CLI options and output fields](artifact/references/options.md)
- [Changelog](artifact/references/changelog.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON]

**Output Format:** [Structured JSON envelope with TikTok video, creator post, or comment records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results vary by command and may be empty; video playback URLs may expire.]

## Skill Version(s):

1.1.3 (source: frontmatter, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
