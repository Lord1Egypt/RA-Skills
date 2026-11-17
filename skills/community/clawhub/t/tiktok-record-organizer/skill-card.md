## Description:

Retrieves public TikTok search results, creator posts, and video comments as structured data for content and engagement analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, marketers, and research teams use this skill to review public TikTok videos, creator activity, and comments for content planning, competitor tracking, and audience analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords and TikTok targets are sent to the GUAIKEI service, and API use may incur fees.

Mitigation: Use a dedicated GUAIKEI token and review the provider's fees and handling of submitted queries and targets.

Risk: When optional logging is enabled, queries and public profile or comment data are saved locally.

Mitigation: Leave logging disabled unless local copies are needed, and protect any generated log files.

## Reference(s):

- [GUAIKEI service](https://www.guaikei.com)
- [ClawHub skill release](https://clawhub.ai/why20261/skills/tiktok-record-organizer)
- [Command options](artifact/references/options.md)
- [Changelog](artifact/references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Data]

**Output Format:** [Structured JSON output envelope containing TikTok search, creator-post, or comment results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public data; results depend on availability and the token plan's request limits.]

## Skill Version(s):

1.1.1 (source: release evidence, SKILL.md frontmatter, package.json, changelog 2026-11-04)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
