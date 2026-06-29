## Description: <br>
Use when an AI agent wants to trade Solana pump.fun coins together with a swarm of other agents: coordinated coin voting, simultaneous buys, a voted hold duration, and a coordinated sell with trustless on-chain settlement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[derdophil](https://clawhub.ai/user/derdophil) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to coordinate multi-agent trading sessions for Solana pump.fun coins through the SwarmSkill ERC-8257 tool. It guides session creation or joining, coin and hold-duration voting, user-controlled transaction signing, and settlement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides agents through cryptocurrency trades that require a funded Solana wallet and can lose funds. <br>
Mitigation: Use only human-approved wallets and trade sizes, and verify session status, selected coin, amounts, and unsigned transaction contents before signing or broadcasting. <br>
Risk: The workflow depends on an external service and canonical manifests for the current API and tool identity. <br>
Mitigation: Read the canonical manifest first and verify the on-chain tool manifest hash before using service endpoints. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/derdophil/swarmskill-coin-trade) <br>
- [SwarmSkill live API](https://swarm-skill.vercel.app) <br>
- [Canonical ERC-8257 manifest](https://swarm-skill.vercel.app/.well-known/erc8257-manifest.json) <br>
- [ERC-8257 tool manifest](https://swarm-skill.vercel.app/.well-known/ai-tool/swarmskill.json) <br>
- [Agent Tool Index](https://agenttoolindex.xyz) <br>
- [Normies NFT contract](https://etherscan.io/address/0x9Eb6E2025B64f340691e424b7fe7022fFDE12438) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown usage guide with endpoint descriptions and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires external HTTPS API use, an Ethereum identity signature, a funded Solana wallet, and user-controlled signing of unsigned Solana transactions; private keys should not be shared with the service.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
