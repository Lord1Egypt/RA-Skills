## Description:

Helps teams identify and evaluate TikTok creators for collaboration using public keyword search, creator posts, and video comment data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

For creators, brands, and marketing teams researching TikTok content, reviewing creator accounts, and preparing data-backed collaboration shortlists from public posts and comments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment is qualified: 20 of 34 components were fully scanned, and the tool-misuse analyzer was degraded.

Mitigation: Review the remaining script behavior and reassess before relying on the skill in sensitive workflows.

Risk: Search terms and TikTok URLs are sent to GUAIKEI's data service to retrieve results.

Mitigation: Use public data you are authorized to analyze and confirm that external data sharing fits your organization's requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/why20261/skills/tiktok-creator-screening)
- [GUAIKEI service and API access](https://www.guaikei.com)
- [Usage options](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Text]

**Output Format:** [Structured JSON response envelopes containing TikTok search results, creator posts, or video comments; concise agent-written analysis when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are limited to public TikTok data and the requested count; availability depends on the query and API plan.]

## Skill Version(s):

1.1.2 (source: frontmatter, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
