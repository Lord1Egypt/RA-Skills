## Description:

Research public TikTok search results, creator posts, and video comments to identify content and market opportunities for further validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

Creators, marketers, and research teams use this skill to explore public TikTok content, compare creator posts, and review video comments for topic research, competitor monitoring, and audience feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was only partially complete, so some scripts were not fully interpreted.

Mitigation: Review the source and consider the scan uncertainty before installation.

Risk: Search terms or TikTok links are sent to guaikei.com, and returned public data may include usernames.

Mitigation: Send only queries suitable for that service, and redact usernames before sharing results externally.

Risk: The skill formats timestamps using Beijing time.

Mitigation: Treat returned timestamps as Beijing time when comparing activity across time zones.

## Reference(s):

- [GUAIKEI TikTok data service](https://www.guaikei.com)
- [ClawHub skill release](https://clawhub.ai/why20261/skills/tiktok-opportunity-research)
- [CLI options](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON]

**Output Format:** [Structured JSON results envelope]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns public TikTok search results, creator posts, or video comments with available engagement fields, depending on the request.]

## Skill Version(s):

1.1.1 (source: server-resolved release, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
