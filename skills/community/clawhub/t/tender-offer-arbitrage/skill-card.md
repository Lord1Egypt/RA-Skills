## Description:

Scans active tender offers, verifies key terms in public filings, calculates tender spread and odd-lot scenarios, and produces a Chinese investment analysis report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[d-wwei](https://clawhub.ai/user/d-wwei)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to research current tender-offer arbitrage opportunities, compare spreads and odd-lot treatment, and prepare a structured Markdown report for review. It supports financial analysis workflows but should not be treated as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tender-offer terms, prices, deadlines, and broker participation requirements can change or be misread.

Mitigation: Verify SEC filings, live market prices, offer deadlines, odd-lot language, proration terms, and brokerage instructions independently before acting.

Risk: The generated report is financial analysis and may be mistaken for personalized investment advice.

Mitigation: Treat the output as research support only and require human review before making investment decisions.

Risk: The skill produces Chinese report output, which can create review risk for users who cannot read Chinese comfortably.

Mitigation: Use reviewers who can read the generated Chinese report or translate and verify the analysis before relying on it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/d-wwei/skills/tender-offer-arbitrage)
- [SEC EDGAR SC TO filing search](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&type=SC+TO&dateb=&owner=include&count=40&search_text=&action=getcompany)
- [InsideArbitrage tender offers](https://www.insidearbitrage.com/tender-offers/)
- [MarketBeat tender offers](https://www.marketbeat.com/corporate-events/tender-offers/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report in Chinese with tables, calculations, rankings, and risk notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes the report under results/YYYY-MM-DD/report.md when the agent follows the skill workflow.]

## Skill Version(s):

2.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
