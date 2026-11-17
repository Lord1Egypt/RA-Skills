## Description:

Sports Betting helps an agent browse Polygon sports markets through Pinwin and Azuro, then place, monitor, and claim on-chain bets when the user explicitly requests it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skinnynoizze](https://clawhub.ai/user/skinnynoizze)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to browse decentralized sports markets, place Pinwin/Azuro bets on Polygon, monitor bet status, and claim winnings from a wallet they control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can sign and submit real-money wallet transactions using BETTOR_PRIVATE_KEY.

Mitigation: Use a dedicated low-balance betting wallet, keep the private key outside agent-readable config when possible, and require explicit confirmation before every transaction.

Risk: A confirmation-bypass flag can skip the interactive confirmation in the betting script.

Mitigation: Do not use the bypass flag for normal operation; manually review the decoded payload, stake, odds, fees, addresses, and transaction before signing.

Risk: Pinwin/Azuro remote payloads and market data may have validation gaps.

Mitigation: Treat remote payloads as trusted only after checking condition, outcome, stake, odds, relayer fee, contract addresses, and current market state.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/skinnynoizze/skills/sports-betting)
- [Publisher Profile](https://clawhub.ai/user/skinnynoizze)
- [Pinwin](https://pinwin.xyz)
- [Azuro Data Feed](https://api.onchainfeed.org/api/v1/public/market-manager/)
- [Azuro Bets Subgraph](https://thegraph.onchainfeed.org/subgraphs/name/azuro-protocol/azuro-api-polygon-v3)
- [Polygonscan Transaction Lookup](https://polygonscan.com/tx/{txHash})

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and script JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node and BETTOR_PRIVATE_KEY; can initiate Polygon wallet signing and transactions only after explicit user confirmation.]

## Skill Version(s):

1.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
