## Description:

Search public TikTok videos by keyword, retrieve a creator’s public posts, and collect comments from a video; the skill returns structured JSON without logging in or publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guaikei](https://clawhub.ai/user/guaikei)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to research public TikTok content for topic discovery, creator monitoring, influencer selection, and comment analysis. It returns video, creator-post, or comment data for an agent to summarize or analyze.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner reports medium confidence because 12 of 34 components were only partly inspected, and its guidance notes timezone behavior.

Mitigation: Review the package before installation and confirm date and time assumptions before relying on time-filtered results.

Risk: The supplied keyword or TikTok link is sent to guaikei.com when the API is called.

Mitigation: Use public TikTok links and avoid putting private or sensitive information in queries.

## Reference(s):

- [Guaikei TikTok API and token setup](https://www.guaikei.com)
- [Usage options](artifact/references/options.md)
- [Frequently asked questions](artifact/references/faq.md)
- [ClawHub skill release](https://clawhub.ai/guaikei/skills/tiktok-search-api)

## Skill Output:

**Output Type(s):** [JSON]

**Output Format:** [Structured JSON response envelope on stdout]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns public video, creator-post, or comment data; empty results are possible, and a returned cost is an estimate.]

## Skill Version(s):

1.1.3 (source: server release evidence, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
