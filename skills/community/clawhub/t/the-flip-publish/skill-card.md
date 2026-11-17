## Description:

$1 USDC entry. 14 coin flips. Get all 14 right, take the entire jackpot. Live on Solana devnet - continuous game, enter anytime.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maurodelazeri](https://clawhub.ai/user/maurodelazeri)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and agents use this skill to enter, operate, inspect, and claim outcomes in a continuous Solana devnet coin-flip game. It provides command-line workflows and API reference material for game status, ticket checks, flips, entries, and claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles wallet signing and token movement for a devnet blockchain game.

Mitigation: Use a dedicated devnet-only wallet with no mainnet funds, avoid passing sensitive keypair paths, and review every transaction before signing.

Risk: The evidence security summary says game fairness and operator controls are under-disclosed.

Mitigation: Treat odds, randomness, anti-rug, and solvency claims as unverified until the program and dependencies have been independently reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maurodelazeri/skills/the-flip-publish)
- [Project homepage](https://github.com/maurodelazeri/the-flip-publish)
- [Dashboard](https://the-flip.vercel.app)
- [Game state API](https://the-flip.vercel.app/api/game)
- [Solana devnet program](https://explorer.solana.com/address/7rSMKhD3ve2NcR4qdYK5xcbMHfGtEjTgoKCS5Mgx9ECX?cluster=devnet)
- [README.md](README.md)
- [IDL](idl/the_flip.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May prompt agents to run Node.js commands that read a local Solana keypair and submit devnet transactions.]

## Skill Version(s):

2.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
