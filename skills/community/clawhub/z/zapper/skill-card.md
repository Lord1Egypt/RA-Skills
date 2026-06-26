## Description: <br>
Query DeFi portfolio data across 50+ chains via Zapper's GraphQL API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spirosrap](https://clawhub.ai/user/spirosrap) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to query wallet balances, DeFi positions, NFT holdings, token prices, transaction history, and unclaimed rewards through Zapper's GraphQL API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried wallet addresses and portfolio-related requests are sent to Zapper. <br>
Mitigation: Use the skill only for wallet addresses and portfolio queries you are comfortable sharing with Zapper. <br>
Risk: The skill stores a Zapper API key in a local configuration file. <br>
Mitigation: Use a dedicated, revocable API key and restrict permissions on the local config file. <br>
Risk: Placing wallet private keys or seed phrases in the skill configuration would expose sensitive credentials. <br>
Mitigation: Store only the Zapper API key in the config and never add private keys or seed phrases. <br>


## Reference(s): <br>
- [Zapper API Reference](references/api.md) <br>
- [Zapper](https://zapper.xyz) <br>
- [Zapper API Docs](https://build.zapper.xyz/docs/api) <br>
- [Zapper Dashboard](https://dashboard.zapper.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and terminal text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local Zapper API key configuration and sends wallet-address queries to Zapper.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
