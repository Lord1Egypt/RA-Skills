## Description:

Swap tokens on Solana via Jupiter aggregator and check wallet balances. Use when user wants to swap tokens, check SOL/token balance, or get swap quotes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imthatcarlos](https://clawhub.ai/user/imthatcarlos)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to inspect Solana wallet balances, request Jupiter swap quotes, and execute confirmed token swaps from a configured wallet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A swap can execute from terms the user did not explicitly approve if the quote is refreshed after confirmation.

Mitigation: Require the agent to build the transaction from the exact approved quote, or display any refreshed quote and request confirmation again before signing.

Risk: The skill operates with a Solana wallet keypair and can move funds.

Mitigation: Use only a wallet intended for trading through this skill, confirm balances and swap details before execution, and avoid exposing private key material.

Risk: Temporary quote and swap files may be unsafe on shared machines.

Mitigation: Review and improve temporary-file handling before use on shared systems.

Risk: The documented signing flow depends on a signer script that is not present in the artifact.

Mitigation: Do not execute swaps until the signer script is supplied and reviewed.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/imthatcarlos/skills/solana-swaps)
- [Jupiter quote API endpoint used by the skill](https://api.jup.ag/swap/v1/quote?inputMint=${INPUT_MINT}&outputMint=${OUTPUT_MINT}&amount=${AMOUNT}&slippageBps=${SLIPPAGE_BPS})
- [Jupiter swap API endpoint used by the skill](https://api.jup.ag/swap/v1/swap)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, API Calls, Guidance]

**Output Format:** [Markdown with inline bash commands and transaction status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces wallet balance summaries, swap quote details, confirmation prompts, transaction signatures, and Solscan links.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
