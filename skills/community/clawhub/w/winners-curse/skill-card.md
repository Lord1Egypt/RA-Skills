## Description:

In a common-value auction where all bidders estimate the same uncertain value, this skill helps an agent explain the winner's curse, condition estimates on winning, and produce a pre-committed bid ceiling or bid floor for contested decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deciqai](https://clawhub.ai/user/deciqai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, founders, operators, procurement teams, and acquisition decision-makers use this skill to avoid overbidding in common-value auctions and competitive processes. It guides agents to classify value uncertainty, count bidders, condition valuation on winning, and return a disciplined walk-away ceiling or bid floor.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat the skill's output as authority to place bids, make acquisitions, or commit capital automatically.

Mitigation: Use the output as decision support only; require qualified human review of auction facts, valuation assumptions, and cited sources before material financial action.

Risk: The winner's curse discipline can be misapplied to private-value goods, single-buyer negotiations, or situations where value is known with near certainty.

Mitigation: Apply the stop rule first: confirm the value is shared and uncertain, otherwise redirect to the appropriate negotiation or valuation framework.

Risk: Competitive pressure, sunk costs, or ego can cause users to override the generated bid ceiling or bid floor.

Mitigation: Pre-commit the ceiling or floor in writing, name an owner authorized to walk away, and reopen it only when new value information arrives.

## Reference(s):

- [Primary Sources](references/sources.md)
- [Offshore Oil-Lease Auctions Example](examples/offshore-oil-lease-auctions-capen-clapp-campbell-1971.md)
- [3G Spectrum Auctions Example](examples/3g-spectrum-auctions-2000.md)
- [HP-Autonomy Acquisition Example](examples/hp-autonomy-acquisition-2011.md)
- [SMB Fixed-Price Bidding Example](examples/smb-construction-bid-winners-curse.md)
- [Competitive Bidding in High-Risk Situations](https://onepetro.org/JPT/article/23/06/641/163651/Competitive-Bidding-in-High-Risk-Situations)
- [Anomalies: The Winner's Curse](https://www.aeaweb.org/articles?id=10.1257/jep.2.1.191)
- [Naturally Occurring Markets and Exogenous Laboratory Experiments](https://ideas.repec.org/a/ecj/econjl/v118y2008i528p822-843.html)
- [Common Value Auctions and the Winner's Curse](https://press.princeton.edu/books/ebook/9781400830138/common-value-auctions-and-the-winners-curse)
- [A Theory of Auctions and Competitive Bidding](https://doi.org/10.2307/1911865)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown bid discipline card with concise analysis and checklist-style gates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask stepwise clarification questions before producing a bid ceiling when key auction inputs are missing.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
