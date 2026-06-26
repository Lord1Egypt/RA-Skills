## Description: <br>
A Stellar USDC wallet skill for AI agents that pays for 402-gated APIs through MPP Router or x402 facilitators, checks balances, manages USDC trustlines, swaps XLM to USDC, and sends or bridges USDC cross-chain via Rozo. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shawnmuggle](https://clawhub.ai/user/shawnmuggle) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to give agents a limited Stellar hot wallet for paid API calls, balance checks, trustline setup, XLM-to-USDC swaps, and cross-chain USDC transfers. It is intended for users who can manage wallet credentials and verify payment details before signing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: This skill can move real USDC from a Stellar hot wallet. <br>
Mitigation: Use a fresh limited-balance wallet, test with --network testnet where supported, and manually verify destination chain, address, amount, memo, and fees before confirming a transaction. <br>
Risk: Mainnet is the default network for normal wallet operations. <br>
Mitigation: Pass --network testnet while prototyping and avoid funding the wallet with more than the session requires. <br>
Risk: Automated payment flags can bypass per-payment confirmation. <br>
Mitigation: Avoid --yes and --max-auto on mainnet unless the transaction is independently verified, and keep any session automation limit low. <br>
Risk: A paid API challenge can direct funds to an unexpected recipient or amount. <br>
Mitigation: Use --expect-pay-to, --expect-amount, and --expect-asset for paid API calls so mismatched payment challenges abort before signing. <br>
Risk: Wallet credentials are sensitive and can be misused if exposed. <br>
Mitigation: Store keys in a mode-600 secret file or Stellar CLI identity, never paste secrets into chat or untrusted UIs, and keep main-wallet secrets out of local dotenv files. <br>


## Reference(s): <br>
- [MPP Router](https://www.mpprouter.dev/) <br>
- [Skill Repository](https://github.com/mpprouter/stellar-agent-wallet-skill) <br>
- [Mainnet checklist](references/mainnet-checklist.md) <br>
- [x402 Stellar exact scheme wire format](references/x402-exact-spec.md) <br>
- [@stellar/mpp charge mode wire format](references/mpp-charge-spec.md) <br>
- [Sponsored mode](references/sponsored-mode.md) <br>
- [SDK API cheatsheet](references/sdk-api-cheatsheet.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, API calls] <br>
**Output Format:** [Markdown with inline shell commands and JSON-capable command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate or use a local Stellar secret file, signed transaction XDR, payment receipts, balance summaries, and cross-chain payment status details.] <br>

## Skill Version(s): <br>
1.7.6 (source: server release metadata; artifact frontmatter and package.json report 1.7.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
