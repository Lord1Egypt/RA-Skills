## Description: <br>
Trade HIP-3 markets on trade.xyz via CAI using Hyperliquid Route B tools for xyz:SYMBOL assets, with CAI API credentials and platform or full API scope. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bernardtai](https://clawhub.ai/user/bernardtai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to guide CAI-assisted trade.xyz HIP-3 market activity, including placing, checking, and cancelling xyz:SYMBOL orders through the CAI Hyperliquid route. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide live CAI/Hyperliquid trading actions that may create losses, fees, liquidation risk, or unintended exposure. <br>
Mitigation: Require the user to review and explicitly confirm every order, cancellation, size, price, asset, and direction before any account-affecting action. <br>
Risk: The skill requires sensitive CAI API credentials and may require platform or full API scope. <br>
Mitigation: Use the least-privileged API scope available, store credentials only through the approved secrets mechanism, and rotate or revoke credentials when access is no longer needed. <br>
Risk: Incorrect asset symbols, dex parameters, or order identifiers can route actions to the wrong market or cancel the wrong order. <br>
Mitigation: Validate xyz:SYMBOL assets, dex values, order identifiers, and account readiness against CAI or Hyperliquid status data before submitting trade actions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/bernardtai/trade-xyz-with-cai) <br>
- [CAI skill reference, section 6.1b](https://cai.com/skill.md) <br>
- [trade.xyz Hyperliquid XYZ and HIP-3 documentation](https://docs.trade.xyz/about-trade-xyz/hyperliquid-xyz-and-hip-3) <br>
- [CAI developers documentation](https://cai.com/developers.html) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline shell commands and structured trade parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes CAI API key setup and trade/order parameter guidance for Hyperliquid Route B tools.] <br>

## Skill Version(s): <br>
1.0.15 (source: release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
