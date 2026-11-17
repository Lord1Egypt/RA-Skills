## Description:

Web3-Crypto-Degen helps agents research tokens, inspect wallet and market data, assess token safety, and prepare or execute DEX and spot-exchange trading workflows across supported Web3 providers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stanpoldark](https://clawhub.ai/user/stanpoldark)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to support Web3 token discovery, market analysis, wallet review, safety checks, and crypto trade preparation or execution across OKX, Binance, Gate.io, Bitget, and supported chains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad exchange credentials and raw wallet private keys, which can create financial risk even for read-only use.

Mitigation: Separate read-only analytics from execution and provide only the single provider credential needed for the current task.

Risk: Live exchange or on-chain execution can move funds if powerful credentials or funded wallets are configured.

Mitigation: Use withdrawal-disabled trade-only exchange keys with IP allowlisting, dedicated minimal-balance wallets, testnet-first validation, and vault-backed mainnet key handling.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stanpoldark/skills/web3-crypto-ops-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code snippets, configuration examples, API call patterns, and concise decision summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Risk flags are expected first; blocked trades should include the reason and alternatives; raw secrets should not be returned.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
