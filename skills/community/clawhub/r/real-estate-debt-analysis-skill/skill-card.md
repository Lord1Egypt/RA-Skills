## Description:

Analyzes real-estate debt portfolios by comparing intermediary listing prices with judicial-auction price estimates to support investment review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yejinlei](https://clawhub.ai/user/yejinlei)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and real-estate analysts use this skill to evaluate property-backed debt portfolios, compare listing and auction price signals, calculate coverage and discount metrics, and produce investment-oriented summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may present generated price estimates as real market or auction data for financial decisions.

Mitigation: Treat outputs as heuristic analysis and independently verify prices, auction records, coverage ratios, and recommendations against current primary sources before acting.

Risk: Property and debt records may be confidential, and the evidence flags unresolved logging, privacy disclosure, and data provenance concerns.

Mitigation: Avoid submitting confidential records, or redact sensitive fields, until logging behavior, privacy handling, and source provenance are reviewed.

Risk: Fallback city prices, random fluctuations, and incomplete auction data can distort investment recommendations.

Mitigation: Require source timestamps, disclose estimation limits, and route final legal, appraisal, and investment decisions through qualified reviewers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yejinlei/skills/real-estate-debt-analysis-skill)
- [Publisher profile](https://clawhub.ai/user/yejinlei)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Configuration]

**Output Format:** [JSON analysis results with summaries, risk assessments, investment suggestions, and optional report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts direct property data and parsed table, text, image, audio, or multimodal inputs.]

## Skill Version(s):

v1.1.0 (source: evidence release; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
