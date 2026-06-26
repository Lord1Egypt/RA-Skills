## Description: <br>
Swap or trade tokens via decentralized exchanges on supported chains using authenticated wallet commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rachidjarray-hk-qa-fdt](https://clawhub.ai/user/rachidjarray-hk-qa-fdt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to prepare and execute token swaps through decentralized exchanges after confirming authentication, balances, token identifiers, amounts, chain, and slippage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can execute real crypto trades from an authenticated wallet. <br>
Mitigation: Require human confirmation of the chain, token symbols or contract addresses, input amount, expected output, and slippage before approving a swap. <br>
Risk: A vague request for token information could be interpreted as permission to swap. <br>
Mitigation: Use explicit wording for price, balance, or general token questions when no trade should be executed. <br>
Risk: Insufficient balance, unavailable liquidity, or slippage can cause a swap to fail or produce a different output than expected. <br>
Mitigation: Check wallet authentication and balances first, use explicit token identifiers where needed, and set max slippage for sensitive or large swaps. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rachidjarray-hk-qa-fdt/swap-tokens) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces fdx status, wallet overview, and swapTokens command guidance; does not define a structured machine-readable output format.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
