## Description: <br>
Defi Yield helps agents compare DeFi yield opportunities, analyze protocol APYs and risks, and suggest yield strategies for assets such as stablecoins, ETH, and BTC. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenmeng](https://clawhub.ai/user/shenmeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and DeFi analysts use this skill to look up APYs, compare yield pools across protocols, and produce strategy guidance based on asset type and risk preference. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled scripts may make SkillPay balance and charge requests before running yield functionality. <br>
Mitigation: Review the scripts before execution and do not set SKILLPAY_USER_ID or run the bundled scripts unless you intentionally accept the SkillPay charge behavior. <br>
Risk: Yield lookups or position-related inputs may expose wallet addresses or query data to third-party API and RPC services. <br>
Mitigation: Avoid providing wallet addresses unless you accept third-party API/RPC exposure, and use non-sensitive addresses or read-only workflows where possible. <br>
Risk: APY and strategy recommendations may be stale, incomplete, or unsuitable for a user's risk tolerance. <br>
Mitigation: Treat outputs as informational and verify current rates, protocol risks, liquidity, and fees directly with the relevant protocols before making financial decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/shenmeng/shenmeng-defi-yield) <br>
- [Yearn Vaults](https://yearn.finance/vaults) <br>
- [Beefy Vaults](https://beefy.finance/vaults) <br>
- [Pendle](https://pendle.finance) <br>
- [Gamma Strategies](https://gamma.xyz) <br>
- [DeFiLlama Yields](https://defillama.com/yields) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with optional Python command examples and tabular APY output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [APY and strategy results are informational and may depend on third-party DeFi APIs.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
