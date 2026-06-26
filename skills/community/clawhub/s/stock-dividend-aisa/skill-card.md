## Description: <br>
Analyze read-only dividend metrics for stocks via the AIsa API, including yield, payout ratio, growth CAGR, safety score, income rating, and Dividend Aristocrat or King status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baofeng-tech](https://clawhub.ai/user/baofeng-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and developers use this skill to request read-only dividend research for one or more stock tickers and receive dividend metrics, safety assessment, income rating, and comparison output. It is for informational analysis and does not connect to brokerage accounts or place trades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ticker symbols and analysis prompts are sent to AIsa or a configured AIsa-compatible endpoint. <br>
Mitigation: Use the default HTTPS endpoint or only a trusted AISA_BASE_URL, and avoid entering confidential investment or personal account details. <br>
Risk: The skill requires an AISA_API_KEY for API access. <br>
Mitigation: Store the key in the environment, prefer a scoped key where available, and do not provide brokerage, payment, cookie, or trading credentials. <br>
Risk: Dividend analysis may be incorrect, stale, or unsuitable as investment advice. <br>
Mitigation: Treat results as informational only and verify financial decisions against trusted market data and qualified advice. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/baofeng-tech/stock-dividend-aisa) <br>
- [Publisher Profile](https://clawhub.ai/user/baofeng-tech) <br>
- [AIsa Homepage](https://aisa.one) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown dividend analysis report with optional structured JSON summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts one or more validated ticker symbols; requires AISA_API_KEY and may use AISA_MODEL or AISA_BASE_URL when configured.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
