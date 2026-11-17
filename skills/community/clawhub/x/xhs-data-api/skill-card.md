## Description:

Analyzes Xiaohongshu content markets for content landscape, creator collaboration, brand competition, and market-opportunity questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sxcvicky](https://clawhub.ai/user/sxcvicky)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing strategists, brand teams, and agency analysts use this skill to analyze Xiaohongshu content strategy, creator fit, competitor activity, and market demand from API-backed sample data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Marketing queries, keywords, brand names, creator names, and related planning context are sent to the analytics API provider.

Mitigation: Use only with a trusted XHS_API_KEY provider and avoid confidential campaign plans or regulated personal data unless approved by the organization.

Risk: Analysis is based on sample coverage and may contain data gaps.

Mitigation: Require outputs to cite _coverage.coverageNote and disclose non-empty _dataGaps before making recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sxcvicky/skills/xhs-data-api)
- [Publisher profile](https://clawhub.ai/user/sxcvicky)
- [Aggregate API reference](references/aggregate-api.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Chinese Markdown analysis with API-backed data findings, recommendations, coverage notes, and data-gap disclosures.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires XHS_API_KEY and uses API responses that include _coverage and _dataGaps fields.]

## Skill Version(s):

0.3.0 (source: release metadata; artifact frontmatter reports 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
