## Description:

Zhiqiu is a Chinese industry-analysis agent that guides market landscape, value chain, competition, strategic group, trend, and risk analysis with optional report-fetching support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tuobadaidai](https://clawhub.ai/user/tuobadaidai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and strategy teams use this skill to produce structured industry research reports, quick scans, industry comparisons, or tracking updates without anchoring the analysis to a specific company.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional financial-report-fetcher dependency is referenced without a pinned immutable version.

Mitigation: Review the dependency publisher and version before installation; skip that dependency and use ordinary current-data search when only quick analysis is needed.

Risk: Industry analysis can become misleading when market, share, price, penetration, or policy data is stale.

Mitigation: Follow the skill's stated recency rules, label data sources and collection dates, and refresh expired or conflicting data before relying on conclusions.

## Reference(s):

- [Zhiqiu ClawHub skill page](https://clawhub.ai/tuobadaidai/skills/zhiqiu)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown reports with tables, structured analysis sections, and optional shell install commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs emphasize source-labeled data, recency checks, cross-validation, and concise industry judgments.]

## Skill Version(s):

1.2.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
