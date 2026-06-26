## Description: <br>
Tator Trader helps agents prepare natural-language crypto trading requests for Tator's AI trading API and review unsigned transaction responses before a user signs or broadcasts them. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[azep-ninja](https://clawhub.ai/user/azep-ninja) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent developers use this skill to construct crypto trade, swap, bridge, transfer, yield, prediction market, token launch, and name-registration requests through Tator, then inspect unsigned transactions before signing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary says wallet broadcast examples could execute irreversible transactions without a clear required user approval step. <br>
Mitigation: Require explicit user approval before every signature or broadcast, and verify recipient, spender, chain, value, approvals, calldata, slippage, fees, and expected outcome before signing. <br>
Risk: The skill connects to a paid external crypto transaction builder. <br>
Mitigation: Use a small dedicated wallet, prefer managed wallet integrations, never provide private keys or seed phrases, and confirm payment and trade details before each request. <br>


## Reference(s): <br>
- [Tator Trader ClawHub Page](https://clawhub.ai/azep-ninja/tator-trader) <br>
- [Publisher Profile](https://clawhub.ai/user/azep-ninja) <br>
- [Tator Docs](https://docs.quickintel.io/tator) <br>
- [x402 Protocol](https://www.x402.org) <br>
- [Tator x402 Payment & Integration Reference](references/REFERENCE.md) <br>
- [Supported Chains Reference](references/chains.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with JSON, JavaScript, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces unsigned transaction-handling guidance; users must review, sign, and broadcast transactions outside the skill.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
