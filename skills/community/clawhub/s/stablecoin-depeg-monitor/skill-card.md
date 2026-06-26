## Description: <br>
Monitor stablecoin peg stability, price-deviation alerts, and historical depeg context for major assets including USDT, USDC, DAI, USDe, and FDUSD. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zuoyeweb3](https://clawhub.ai/user/zuoyeweb3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and crypto risk analysts use this skill to check stablecoin peg-health signals, summarize depeg history, and receive practical monitoring guidance. The skill is informational and should be cross-checked against independent market and issuer sources before financial decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stablecoin safety labels may overstate what the documented Barker API data can support. <br>
Mitigation: Treat the skill's peg status as informational and verify live prices, liquidity, and issuer communications with independent DEX, CEX, or issuer sources before making financial decisions. <br>
Risk: The skill depends on Barker as a third-party market data source. <br>
Mitigation: Use the Barker API as one input among multiple sources and account for rate limits, outages, or incomplete market coverage. <br>


## Reference(s): <br>
- [Stablecoin Depeg Monitor on ClawHub](https://clawhub.ai/zuoyeweb3/stablecoin-depeg-monitor) <br>
- [Barker](https://barker.money) <br>
- [Barker Public Stablecoin Market API](https://api.barker.money/api/public/v1/stablecoin-market) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown status tables and concise guidance with optional API-backed market summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Informational stablecoin risk summaries; no files are produced by the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
