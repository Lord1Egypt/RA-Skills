## Description:

This skill retrieves public TikTok search results, creator posts, and video comments, then returns structured JSON for operational analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

TikTok creators, brand operators, and market analysts can use the skill to research content ideas, monitor public competitor posts, and summarize discussion in video comments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and targeted TikTok links are sent to the third-party data provider, and API calls may incur charges.

Mitigation: Use a dedicated API token, avoid sending sensitive query details, and review provider billing terms before making large requests.

Risk: Optional result logs may retain retrieved data on the local machine.

Mitigation: Leave local logging disabled unless needed and protect any saved results.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/why20261/skills/tiktok-yunying-zhushou)
- [Guaikei data service and token support](https://www.guaikei.com)
- [Command options](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Structured data]

**Output Format:** [JSON envelope containing video search results, creator posts, or comments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public data; empty results are valid, some fields may be absent, and playback URLs may expire.]

## Skill Version(s):

1.1.1 (source: frontmatter, changelog released 2026-11-04, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
