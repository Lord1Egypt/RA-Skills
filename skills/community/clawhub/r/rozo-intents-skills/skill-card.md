## Description: <br>
Cross-chain crypto payments and bridging via Rozo for USDC and USDT across Ethereum, Base, BNB Chain, Solana, Stellar, Arbitrum, and Polygon, including balance checks, QR parsing, payment creation, and payment status lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shawnmuggle](https://clawhub.ai/user/shawnmuggle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to route crypto payment intents, check wallet balances, parse payment QR codes, estimate fees, create Rozo payments after confirmation, and track payment status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crypto payment workflows send wallet addresses, balances, transaction hashes, QR payment contents, and payment setup details to external Rozo-operated services. <br>
Mitigation: Install only if that data sharing is acceptable for the intended workflow, and avoid using the skill for unrelated blockchain questions or non-payment tasks. <br>
Risk: Incorrect chain, token, amount, recipient, memo, fee, or total could cause an unintended payment outcome. <br>
Mitigation: Verify all payment details before confirming, ask for the chain when an EVM address is ambiguous, and use the dry-run fee check before creating a payment. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/shawnmuggle/rozo-intents-skills) <br>
- [Rozo API Reference](references/api-reference.md) <br>
- [Supported Chains](references/supported-chains.md) <br>
- [Wallet Address Detection Rules](references/wallet-detection.md) <br>
- [Rozo Payment API](https://intentapiv4.rozo.ai/functions/v1/payment-api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and structured payment, balance, QR parsing, and status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js for bundled scripts and expects explicit user confirmation before creating a payment.] <br>

## Skill Version(s): <br>
1.0.2 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
