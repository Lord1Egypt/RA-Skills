## Description:

Researches current social, consumer, technology, cultural, weather, supply, and perception shifts and maps them to U.S.-listed equities using an evidence-gated social-arbitrage process that produces research biases rather than trade instructions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiahongc](https://clawhub.ai/user/jiahongc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to triage public social, consumer, technology, cultural, weather, supply, and perception shifts into evidence-backed U.S.-listed equity research watchlists. It is intended for current trend reports, trend-to-ticker scans, long/short/neutral research bias mapping, and rejection of weak signals, not trade execution or personalized investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake research bias labels for investment recommendations or trade instructions.

Mitigation: Keep outputs framed as research triage, require dated evidence and falsifiers, and exclude entries, exits, stops, sizing, leverage, options contracts, allocation, brokerage connection, and trade execution.

Risk: Current social or market signals can be manipulated, sponsored, duplicated, anecdotal, or insufficiently corroborated.

Mitigation: Require authenticity checks, alternative explanations, independent corroboration, exposure verification, materiality analysis, and rejection or lower tiering when evidence is weak.

Risk: Account-gated social research or user-provided tips may create privacy, account safety, or MNPI concerns.

Mitigation: Use public or user-authorized sources only, disclose inaccessible channels, avoid private personal information, reject possible MNPI contamination, and never request brokerage credentials or funds access.

## Reference(s):

- [Social Arbitrage Methodology](references/methodology.md)
- [Research and Tool Playbook](references/research-playbook.md)
- [Social Arbitrage Report Contract](references/report-template.md)
- [Investor.gov social-media stock scams](https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/social-media-stock-scams)
- [Investor.gov internet and social-media fraud](https://www.investor.gov/protect-your-investments/fraud/types-fraud/internet-and-social-media-fraud)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown research reports, watchlists, evidence tables, monitoring plans, and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include dated sources, access limitations, research bias labels, counterarguments, falsifiers, and data gaps; outputs should not include trade execution, sizing, options, brokerage access, or personalized investment instructions.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
