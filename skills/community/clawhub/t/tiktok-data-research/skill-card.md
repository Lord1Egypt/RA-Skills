## Description:

Retrieves public TikTok search results, creator videos, and video comments as structured JSON for content research and analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

TikTok creators, marketers, and researchers can retrieve public video search results, creator posts, and comments to support content research, competitor monitoring, and audience analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security analysis was partial: some components were not fully analyzed.

Mitigation: Review the partially analyzed components and confirm the skill's tool scope before deployment.

Risk: Queries use a third-party data service and require an API token.

Mitigation: Protect GUAIKEI_API_TOKEN and review the service's data handling before sending queries; use only data permitted for your intended use.

## Reference(s):

- [TikTok数据智能助手 on ClawHub](https://clawhub.ai/why20261/skills/tiktok-data-research)
- [Guaikei service and token support](https://www.guaikei.com)
- [Command options](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [Structured JSON response envelope containing TikTok search results, creator posts, or video comments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on publicly available data and API responses; fields may be omitted, and video files are not downloaded.]

## Skill Version(s):

1.1.1 (source: SKILL.md frontmatter, package.json, changelog, released 2026-11-04)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
