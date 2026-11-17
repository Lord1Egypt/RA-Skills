## Description:

青虎AI helps agents find current Amazon best sellers and rising product opportunities by filtering product research data on sales, revenue, BSR movement, ratings, reviews, profit, seller structure, and history trends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External marketplace sellers, product researchers, and ecommerce operators use this skill to scan Amazon marketplaces, shortlist high-opportunity products, validate trend momentum, and identify category risks before sourcing or launch decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires access to a Qinghu API token.

Mitigation: Use it only where the token can be provided securely and kept out of shared logs, exports, and transcripts.

Risk: Larger product-research results may be exported to local files automatically.

Mitigation: Run it in workspaces where export paths and cached files are controlled, reviewed, and cleaned up after use.

Risk: Amazon sales, revenue, and trend figures are third-party estimates.

Mitigation: Treat outputs as research signals and cross-check important sourcing or launch decisions against additional data.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/qinghu-amazon-trend-hunter)
- [Qinghu API endpoint](https://www.iqinghu.com/api/desktop/qh/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Shell commands, Code, Files, Configuration, Guidance]

**Output Format:** [Markdown guidance with concise product summaries, API call examples, and exported table files for larger result sets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include data scope such as marketplace, period, time window, and sample size; larger returned record sets may be exported as local table files.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
