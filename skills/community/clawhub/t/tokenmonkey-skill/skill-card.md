## Description: <br>
P2P wagering on Solana for USDC, enabling agents to create and accept coinflip and dice challenges, check results, and manage wagering activity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lifestylearb](https://clawhub.ai/user/lifestylearb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to interact with TokenMonkey wagering flows on Solana, including creating challenges, accepting open challenges, checking balances and stats, claiming winnings, and canceling open challenges. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use wallet-signing authority and spend USDC when provided SOLANA_PRIVATE_KEY. <br>
Mitigation: Use only a dedicated low-balance wallet, require explicit confirmation before signing transactions, and enforce strict spending limits for bets and challenge acceptance. <br>
Risk: Crypto wagering can create financial loss or compliance risk for users and organizations. <br>
Mitigation: Restrict use to permitted environments, prefer devnet or test funds where appropriate, and review each wager against applicable policy before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lifestylearb/tokenmonkey-skill) <br>
- [TokenMonkey homepage](https://tokenmonkey.com) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with TypeScript and bash snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and SOLANA_PRIVATE_KEY configured for a Solana wallet.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
