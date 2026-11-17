## Description:

Fetches X-TechCon technology hot-news items when triggered and returns formatted headlines, summaries, and source links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardtechcon](https://clawhub.ai/user/edwardtechcon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve concise technology news from X-TechCon through supported Chinese-language trigger phrases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Invoking the skill contacts www.x-techcon.com and returns links from that service.

Mitigation: Deploy only where outbound access to X-TechCon is acceptable and users can evaluate third-party news links before opening them.

Risk: The requests dependency is declared without a pinned version.

Mitigation: Pin and review the dependency version before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/edwardtechcon/skills/xtechhotnews)
- [X-TechCon hot news API](https://www.x-techcon.com/api/hot_news)
- [X-TechCon website](https://www.x-techcon.com)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [Plain text with numbered news items and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a fallback message when the user query does not contain a supported trigger phrase or the news request fails.]

## Skill Version(s):

1.0.0 (source: release evidence, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
