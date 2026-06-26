## Description: <br>
THE FLIP is a Solana devnet coin-flip game where a $1 USDC entry buys 20 predictions and matching the first 14 wins the jackpot. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maurodelazeri](https://clawhub.ai/user/maurodelazeri) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agents use this skill to inspect and operate a Solana devnet jackpot game, including checking game status, entering predictions, flipping rounds, checking tickets, and claiming eligible winnings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read a local Solana keypair and sign transactions. <br>
Mitigation: Use a dedicated devnet-only wallet and require explicit approval before running commands that enter, claim, flip, initialize, withdraw fees, or close game state. <br>
Risk: Setup includes npm dependencies and a curl-to-shell Solana installer. <br>
Mitigation: Review dependencies and installer commands before execution, and install only in an isolated development environment. <br>
Risk: The game uses transaction and admin-style commands with financial effects on devnet assets. <br>
Mitigation: Confirm the command, wallet, round, and amount before signing any transaction. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/maurodelazeri/the-flip) <br>
- [Project homepage](https://github.com/maurodelazeri/the-flip-publish) <br>
- [Dashboard and API](https://the-flip.vercel.app) <br>
- [Solana devnet program](https://explorer.solana.com/address/7rSMKhD3ve2NcR4qdYK5xcbMHfGtEjTgoKCS5Mgx9ECX?cluster=devnet) <br>
- [README](README.md) <br>
- [Anchor IDL](idl/the_flip.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, json, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON API examples, and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may read a local Solana keypair and sign Solana devnet transactions.] <br>

## Skill Version(s): <br>
1.0.8 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
