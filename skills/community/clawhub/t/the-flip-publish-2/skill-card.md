## Description:

$1 USDC entry. Pick 20 predictions. All 20 coins flip at once each round. Match the first 14 to win the entire jackpot. Live on Solana devnet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bedesta5050](https://clawhub.ai/user/bedesta5050)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to participate in and monitor a Solana devnet coin-flip jackpot game, including checking game status, entering predictions, looking up tickets, triggering flips, and claiming eligible winnings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet-signing and admin actions may be under-disclosed.

Mitigation: Use a disposable Solana devnet keypair, keep mainnet funds out of the environment, and review every wallet-signing transaction before approval.

Risk: Setup includes installer and dependency risks.

Mitigation: Install only in an isolated devnet environment and independently verify curl-piped installers and dependencies before execution.

Risk: The game should not be used for real-value gambling without further fixes.

Mitigation: Limit use to Solana devnet unless randomness, jackpot accounting, dependency vulnerabilities, and admin-command separation are reviewed and fixed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bedesta5050/skills/the-flip-publish-2)
- [Project Homepage](https://github.com/maurodelazeri/the-flip-publish)
- [Live Dashboard](https://the-flip.vercel.app)
- [Solana Devnet Program](https://explorer.solana.com/address/7rSMKhD3ve2NcR4qdYK5xcbMHfGtEjTgoKCS5Mgx9ECX?cluster=devnet)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with command examples and JSON API response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and a disposable Solana devnet wallet for transaction-signing flows.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
