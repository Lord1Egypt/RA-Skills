## Description: <br>
Manage crypto wallets, transfers, swaps, and balances via the Sponge Wallet API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rishabluthra](https://clawhub.ai/user/rishabluthra) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and developers use this skill to register managed Sponge wallets, store API credentials, and call REST endpoints for balances, transfers, swaps, bridge actions, Polymarket trading, x402 payments, and Amazon checkout. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent durable authority over wallet funds, paid API requests, trading, withdrawals, and purchases. <br>
Mitigation: Use testnet or low-balance accounts, require explicit confirmation before value-moving actions, and rotate or revoke the API key when finished. <br>
Risk: Agent-first registration can issue an API key before the human owner has claimed the agent. <br>
Mitigation: Prefer standard human approval for real funds, or keep agent-first wallets unfunded until the owner claim is complete. <br>
Risk: Amazon checkout and x402 fetch can create real-world purchases or automatic payments. <br>
Mitigation: Use checkout dry runs where available and require user confirmation for every checkout or paid fetch. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rishabluthra/wallet-skills) <br>
- [Sponge Wallet homepage](https://wallet.paysponge.com) <br>
- [Sponge Wallet API base](https://api.wallet.paysponge.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with REST endpoint tables and bash/curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SPONGE_API_KEY; agents make JSON REST requests and store credentials in ~/.spongewallet/credentials.json.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
