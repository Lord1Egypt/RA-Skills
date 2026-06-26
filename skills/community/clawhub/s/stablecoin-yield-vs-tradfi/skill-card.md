## Description: <br>
Compare stablecoin DeFi/CEX yields against traditional finance benchmarks such as bank savings, money market funds, and US Treasury bills using Barker yield data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zuoyeweb3](https://clawhub.ai/user/zuoyeweb3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to compare stablecoin yield opportunities with traditional finance alternatives and frame the comparison by risk, liquidity, insurance, and benchmark rates. It is intended for informational yield analysis, not personalized financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Yield comparisons may be mistaken for financial advice or may rely on rates that changed after retrieval. <br>
Mitigation: Present outputs as informational, cite live Barker data where used, and tell users to verify rates with the relevant protocol, exchange, bank, or Treasury source. <br>
Risk: Users may disclose sensitive financial details while asking for personalized comparisons. <br>
Mitigation: Avoid requesting wallet addresses, balances, bank account details, tax identifiers, or other sensitive financial information. <br>


## Reference(s): <br>
- [Barker](https://barker.money) <br>
- [Barker stablecoin APY trend endpoint](https://api.barker.money/api/public/v1/stablecoin-apy-trend?days=30) <br>
- [Barker stablecoin yields endpoint](https://api.barker.money/api/public/v1/stablecoin-yields?asset=usdc&sort=apy&limit=10) <br>
- [ClawHub skill page](https://clawhub.ai/zuoyeweb3/stablecoin-yield-vs-tradfi) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, API Calls, Guidance] <br>
**Output Format:** [Markdown with comparison tables and risk notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May cite live Barker API values and approximate TradFi benchmark rates; outputs should remain informational and include Barker attribution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
