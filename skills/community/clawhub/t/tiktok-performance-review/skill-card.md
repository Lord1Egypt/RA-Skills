## Description:

Fetch public TikTok search results, creator posts, and video comments as structured data for content reviews and strategy analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

Creators, marketers, and developers can research public TikTok content and engagement, compare creators or competitors, and develop testable content strategies from the returned data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan found no confirmed harmful behavior, but its review was partial: 12 of 32 components were only partially inspected.

Mitigation: Review the skill and its scripts before installation, with particular attention to the outbound request and token handling described in its documentation.

Risk: The skill sends the requested TikTok keyword or URL to the GUAIKEI service, and sends the API token in the request.

Mitigation: Use it only when sharing those queries and URLs with the service is acceptable, and keep the token private in the required environment variable.

Risk: Public comment results can include user names and other identifying details.

Mitigation: Review and anonymize identifying details before sharing results outside the team.

## Reference(s):

- [GUAIKEI service and token information](https://www.guaikei.com)
- [Command options](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON]

**Output Format:** [JSON response envelope]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Contains search, creator-post, or video-comment results; available result counts depend on the request and service plan.]

## Skill Version(s):

1.1.1 (source: SKILL.md frontmatter, package.json, changelog; released 2026-11-04)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
