## Description:

Solana wallet operations - create wallets, check balances, send SOL/tokens, swap via Jupiter, launch tokens on Pump.fun

This skill is ready for commercial/non-commercial use.

## Publisher:

[spendit-ai](https://clawhub.ai/user/spendit-ai)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to manage Solana wallets, inspect balances, transfer SOL or SPL tokens, request and execute Jupiter swaps, and launch Pump.fun tokens.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles real Solana funds and defaults transaction-capable workflows toward mainnet use.

Mitigation: Use a dedicated low-value wallet, prefer devnet for testing, and verify the selected network before running transfer, swap, or token launch commands.

Risk: Private keys are stored and loaded through environment variables and .env files.

Mitigation: Do not reuse a wallet holding important funds, avoid sourcing .env files broadly, and prefer a hardware or managed wallet workflow where possible.

Risk: Transaction commands can send funds, swap assets, or launch tokens using user-supplied recipients, amounts, mints, and metadata.

Mitigation: Review every recipient, amount, mint, token symbol, image, custom mint key, and transaction intent before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/spendit-ai/skills/solana-skills)
- [Publisher profile](https://clawhub.ai/user/spendit-ai)
- [Jupiter API portal](https://portal.jup.ag/)
- [Jupiter Ultra API endpoint](https://api.jup.ag/ultra/v1)
- [Solana mainnet RPC endpoint](https://api.mainnet-beta.solana.com)
- [Solana devnet RPC endpoint](https://api.devnet.solana.com)
- [Solana testnet RPC endpoint](https://api.testnet.solana.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and command output text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local wallet configuration and may submit signed Solana transactions when transaction commands are run.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
