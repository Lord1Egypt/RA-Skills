## Description:

TrendProof queries trendproof.dev for keyword trend velocity scores, trend direction, monthly search volume, CPC, peak window, action hints, batch comparisons, and related keyword discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[akvise](https://clawhub.ai/user/akvise)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use TrendProof to check whether keywords, topics, and niches are rising, stable, or falling before creating content, running ads, or planning products.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a TrendProof API key and can save it in local configuration.

Mitigation: Prefer a temporary environment variable or limited API key, and check local config-file permissions when using configure.

Risk: Keyword queries are sent to TrendProof for trend analysis.

Mitigation: Avoid sending sensitive or confidential keywords unless that data sharing is acceptable.

Risk: TRENDPROOF_BASE_URL can redirect requests to a non-default endpoint.

Mitigation: Set TRENDPROOF_BASE_URL only when the endpoint is trusted.

## Reference(s):

- [TrendProof website](https://trendproof.dev)
- [TrendProof analyze API](https://trendproof.dev/api/analyze)
- [TrendProof related keywords API](https://trendproof.dev/api/related)
- [TrendProof public leaderboard API](https://trendproof.dev/api/leaderboard?limit=10&sort=velocity)
- [ClawHub skill page](https://clawhub.ai/akvise/skills/trendproof)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration guidance]

**Output Format:** [Markdown-ready summaries, terminal tables, and optional JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a TrendProof API key for authenticated endpoints; batch analysis accepts multiple keywords and can read newline-separated keyword files.]

## Skill Version(s):

1.2.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
