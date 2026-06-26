## Description: <br>
Stock Research Engine helps an agent produce Chinese-language buy-side style equity research briefs for A-share, Hong Kong, and U.S. stocks from a company name, ticker, or investment analysis request. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ttyyyy8517-ship-it](https://clawhub.ai/user/ttyyyy8517-ship-it) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, analysts, and investing-focused agents use this skill to structure public-market stock research briefs with market sentiment, company fundamentals, management assessment, business drivers, catalysts, risks, and valuation data. It is intended to support research workflows, not to replace primary-source verification or licensed financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may send stock tickers, company names, or user-provided market context to external search or financial data sources. <br>
Mitigation: Avoid submitting sensitive portfolio, trading, or account information unless the connected data sources are approved for that use. <br>
Risk: Market data, financial metrics, and news may be stale, inconsistent, or unavailable across sources. <br>
Mitigation: Verify key figures against primary filings, investor relations materials, and at least two current market data sources before relying on the brief. <br>
Risk: The fund-manager style output may sound confident and could be mistaken for licensed financial advice. <br>
Mitigation: Treat the output as research support only and require human review by an appropriately qualified person before investment decisions. <br>


## Reference(s): <br>
- [Analysis Framework](artifact/references/analysis-framework.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/ttyyyy8517-ship-it/stock-research-engine) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown research brief] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The artifact specifies a 2000-4000 Chinese-character brief with time-stamped financial data, source discipline, fact/opinion separation, and valuation data shown without a buy/sell conclusion.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
