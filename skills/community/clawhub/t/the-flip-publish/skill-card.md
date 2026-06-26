## Description: <br>
$1 USDC entry. 14 coin flips. Get all 14 right, take the entire jackpot. Live on Solana devnet - continuous game, enter anytime. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maurodelazeri](https://clawhub.ai/user/maurodelazeri) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to interact with a Solana devnet coin-flip jackpot game, including checking game status, entering predictions, reviewing tickets, advancing flips, and claiming winnings. Operators can also initialize the game and withdraw operator fees. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read local wallet keypairs and sign fund-moving Solana transactions. <br>
Mitigation: Use a dedicated devnet-only wallet, keep valuable wallets separate, and inspect each transaction before running enter, claim, withdraw-fees, or close-game-v1. <br>
Risk: Setup documentation includes a curl-piped installer for Solana tooling. <br>
Mitigation: Avoid the curl-piped installer unless the upstream source is independently trusted and verified. <br>
Risk: Admin operations such as withdraw-fees and close-game-v1 have limited safeguards. <br>
Mitigation: Restrict operator commands to authorized wallets and review command intent before signing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/maurodelazeri/the-flip-publish) <br>
- [ClawHub metadata homepage](https://github.com/maurodelazeri/the-flip-publish) <br>
- [Game dashboard](https://the-flip.vercel.app) <br>
- [Solana devnet program](https://explorer.solana.com/address/7rSMKhD3ve2NcR4qdYK5xcbMHfGtEjTgoKCS5Mgx9ECX?cluster=devnet) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and a Solana devnet wallet for transaction-signing commands.] <br>

## Skill Version(s): <br>
2.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
