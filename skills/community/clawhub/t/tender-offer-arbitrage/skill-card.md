## Description: <br>
Scans tender-offer arbitrage opportunities, checks official filings and market data, and generates an investment analysis report focused on spreads, odd-lot priority, and transaction risk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[d-wwei](https://clawhub.ai/user/d-wwei) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Investors and financial research agents use this skill to identify active tender offers, verify key terms in SEC filings, calculate potential odd-lot arbitrage returns, and produce a Chinese-language research report. It is intended for research support and requires independent verification before any investment decision. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tender-offer terms, market prices, deadlines, and broker procedures can change or be misread, which may make the generated analysis inaccurate. <br>
Mitigation: Independently verify SEC filings, current prices, tender deadlines, and broker participation rules before relying on the report. <br>
Risk: The skill saves reports locally and repeated runs may create or overwrite research outputs in the results folder. <br>
Mitigation: Review the results directory before rerunning and preserve prior reports when they need to remain available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/d-wwei/tender-offer-arbitrage) <br>
- [SEC EDGAR SC TO filings](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&type=SC+TO&dateb=&owner=include&count=40&search_text=&action=getcompany) <br>
- [InsideArbitrage tender offers](https://www.insidearbitrage.com/tender-offers/) <br>
- [MarketBeat tender offers](https://www.marketbeat.com/corporate-events/tender-offers/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, analysis, files, guidance] <br>
**Output Format:** [Markdown report saved under results/YYYY-MM-DD/report.md] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-language financial research report with tables, calculations, ranked opportunities, action guidance, and disclaimers.] <br>

## Skill Version(s): <br>
2.0.0 (source: ClawHub release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
