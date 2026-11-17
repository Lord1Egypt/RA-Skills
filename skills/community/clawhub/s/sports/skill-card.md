## Description:

Autonomously monitor live sports games and execute micro-bets on one-touch barrier options with instant mockUSDC settlement on Solana Devnet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gigabit-eth](https://clawhub.ai/user/gigabit-eth)

### License/Terms of Use:

MIT

## Use Case:

External developers and agent operators use this skill to connect an agent to Optionns, inspect live sports markets, and execute mockUSDC one-touch barrier option trades on Solana Devnet. It is intended for devnet-only autonomous sports trading workflows with throwaway credentials and mock funds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores API credentials and Solana signing key material locally.

Mitigation: Run it in an isolated environment, use only throwaway Solana Devnet keypairs, and never reuse real wallets or mainnet keys.

Risk: The remote Optionns service can provide blockchain transaction instructions that the local keypair signs.

Mitigation: Verify the API and RPC endpoints, review the signing workflow before use, and avoid autonomous mode unless that trust model is acceptable.

Risk: Autonomous mode can execute repeated devnet betting actions without step-by-step human approval.

Mitigation: Start with inspection and manual trade commands, monitor behavior, and keep operation limited to mock funds on Solana Devnet.

## Reference(s):

- [Optionns API Reference](references/api.md)
- [Optionns Homepage](https://optionns.com)
- [Optionns ClawHub Listing](https://clawhub.ai/gigabit-eth/skills/sports)
- [Solana CLI Installation](https://docs.solanalabs.com/cli/install)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and terminal text or JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local configuration files, API credentials, and Solana Devnet transaction signing.]

## Skill Version(s):

1.0.24 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
