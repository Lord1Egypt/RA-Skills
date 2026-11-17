## Description:

$1 USDC entry. Pick 20 predictions. All 20 coins flip at once each round. Match the first 14 to win the entire jackpot. Live on Solana devnet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maurodelazeri](https://clawhub.ai/user/maurodelazeri)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to inspect, enter, flip, and claim rounds in a Solana devnet coin-flip jackpot game. Developers can also use the included CLI, API examples, IDL, and on-chain account details to integrate or inspect the game state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run an unpinned remote installer during wallet setup.

Mitigation: Review the installer source independently before execution, or install Solana tooling through a pinned and trusted channel.

Risk: The skill operates a fund-moving jackpot flow on Solana devnet.

Mitigation: Use only a throwaway devnet wallet with no real assets, and do not connect production wallets or mainnet funds.

Risk: The scanner summary says the contract behavior is under-disclosed and unsafe for fairness or production use without fixes for randomness and round-specific payout accounting.

Mitigation: Do not treat the jackpot game as fair or production-safe until the smart contract design is reviewed and fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maurodelazeri/skills/the-flip)
- [Project homepage](https://github.com/maurodelazeri/the-flip-publish)
- [Game dashboard](https://the-flip.vercel.app)
- [Solana devnet program](https://explorer.solana.com/address/7rSMKhD3ve2NcR4qdYK5xcbMHfGtEjTgoKCS5Mgx9ECX?cluster=devnet)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [The Flip IDL](artifact/idl/the_flip.json)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Solana devnet command examples, wallet setup guidance, API response examples, and on-chain account references.]

## Skill Version(s):

1.0.8 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
