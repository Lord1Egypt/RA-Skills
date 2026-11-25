## Description:

In a common-value auction where all bidders estimate the SAME uncertain value, the winner is systematically the one who most OVER-estimated it — so winning is bad news that you likely overpaid.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deciqai](https://clawhub.ai/user/deciqai)

### License/Terms of Use:

MIT-0

## Use Case:

Business leaders, founders, and analysts use this skill to assess bids in auctions and competitive deals with shared, uncertain value. It helps them condition estimates on winning, set a value-based walk-away ceiling, and guard against escalation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is partial because one path-like reference in SKILL.md was unresolved.

Mitigation: Locate and review the unresolved reference before relying on the skill or installing it.

Risk: A generalized bid-shading estimate may not fit a private-value or near-certain-value case, or a case where the bidder has a genuine information or cost advantage.

Mitigation: Confirm that the value is shared and uncertain, assess bidder count and estimate dispersion, and account for any documented source of bidding advantage before setting a ceiling.

## Reference(s):

- [Capen, Clapp & Campbell (1971), Competitive Bidding in High-Risk Situations](https://onepetro.org/JPT/article/23/06/641/163651/Competitive-Bidding-in-High-Risk-Situations)
- [Milgrom & Weber (1982), A Theory of Auctions and Competitive Bidding](https://doi.org/10.2307/1911865)
- [Thaler (1988), Anomalies: The Winner's Curse](https://www.aeaweb.org/articles?id=10.1257/jep.2.1.191)
- [Kagel & Levin (2002), Common Value Auctions and the Winner's Curse](https://press.princeton.edu/books/ebook/9781400830138/common-value-auctions-and-the-winners-curse)
- [Winner's Curse skill overview](https://www.deciqai.com/c/winners-curse)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown]

**Output Format:** [Markdown, including a Bid Discipline Card and step-by-step prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Applies only when there are competing bidders and a shared uncertain value; it can guide a bid ceiling but does not supply case-specific valuation inputs.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
