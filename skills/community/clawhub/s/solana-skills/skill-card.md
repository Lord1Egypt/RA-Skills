## Description: <br>
Solana wallet operations - create wallets, check balances, send SOL/tokens, swap via Jupiter, launch tokens on Pump.fun <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spendit-ai](https://clawhub.ai/user/spendit-ai) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to manage Solana wallets, check balances, transfer SOL or SPL tokens, swap tokens through Jupiter, and launch Pump.fun tokens from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent real Solana transaction authority, including mainnet transfers, swaps, and token launches. <br>
Mitigation: Use only a new or low-balance wallet, test on devnet first, and do not expose a valuable private key to an autonomous agent. <br>
Risk: Transfers, swaps, fees, routes, recipients, and token-launch parameters can move funds or create irreversible on-chain actions. <br>
Mitigation: Manually verify every recipient, amount, route, fee, and token launch before execution. <br>
Risk: The artifact includes vanity-address guidance that could be read as implying token legitimacy. <br>
Mitigation: Do not use vanity-address wording or address patterns to imply endorsement, safety, or legitimacy. <br>


## Reference(s): <br>
- [ClawHub Solana skill page](https://clawhub.ai/spendit-ai/solana-skills) <br>
- [Jupiter Ultra API endpoint](https://api.jup.ag/ultra/v1) <br>
- [Jupiter API key portal](https://portal.jup.ag/) <br>
- [Pump.fun](https://pump.fun) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and command-line text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SOLANA_PRIVATE_KEY for wallet authority; Jupiter swaps also require JUPITER_API_KEY.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
