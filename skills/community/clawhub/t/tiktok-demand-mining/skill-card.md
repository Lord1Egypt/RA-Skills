## Description:

Fetch TikTok videos, creator posts, and comments for demand discovery, sentiment analysis, and content research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, marketers, and product teams use this skill to search public TikTok videos, review creator activity, and collect comments for demand, sentiment, and competitor analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The benign security verdict has medium confidence because 12 of 33 components were only partially inspected, including executable scripts.

Mitigation: Review and scan the skill before running it, especially after updates.

Risk: The skill sends GUAIKEI_API_TOKEN to guaikei.com and returns TikTok creator and commenter data that may identify people.

Mitigation: Keep the token private, confirm the external data handling is acceptable, and anonymize identities before sharing results.

## Reference(s):

- [Demand mining workflow](references/demand-mining.md)
- [Command options](references/options.md)
- [Release notes](references/changelog.md)
- [GUAIKEI service and token access](https://www.guaikei.com)
- [ClawHub release page](https://clawhub.ai/why20261/skills/tiktok-demand-mining)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured JSON result envelopes with TikTok video, creator post, or comment data; agent summaries can be written in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the requested filters, available public data, and account plan limits.]

## Skill Version(s):

1.1.2 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
