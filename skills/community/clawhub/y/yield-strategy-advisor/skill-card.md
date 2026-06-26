## Description: <br>
Recommends stablecoin yield strategies based on risk tolerance, capital size, chain preference, and Barker yield data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zuoyeweb3](https://clawhub.ai/user/zuoyeweb3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill to compare stablecoin yield options and draft diversified allocation plans across lending, vault, CEX, and on-chain venues. It is intended for educational strategy guidance, not transaction execution or financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Yield recommendations may be outdated or incomplete because APY values change over time. <br>
Mitigation: Refresh Barker public API data and verify protocol terms, capacity, and current APY before acting. <br>
Risk: Users may treat educational allocation guidance as financial advice or transaction approval. <br>
Mitigation: Present outputs as educational planning guidance and require independent review before moving funds. <br>
Risk: Portfolio details, wallet addresses, credentials, or exact holdings could be shared in conversation unnecessarily. <br>
Mitigation: Avoid requesting sensitive account data and remind users to share only the portfolio details they intentionally want considered. <br>
Risk: Use of DeFi and CEX venues can involve smart contract, liquidity, custody, lockup, and venue-specific risks. <br>
Mitigation: Include strategy-specific risk notes and encourage users to verify audits, TVL, lockups, and venue policies before depositing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zuoyeweb3/yield-strategy-advisor) <br>
- [Barker stablecoin yield map](https://barker.money) <br>
- [Barker public stablecoin yields API](https://api.barker.money/api/public/v1/stablecoin-yields?sort=apy&limit=50) <br>
- [Barker public API root](https://api.barker.money/api/public/v1) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown] <br>
**Output Format:** [Markdown with allocation tables, blended APY estimates, risk notes, and source attribution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference live Barker API data; recommendations should be verified before moving funds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
