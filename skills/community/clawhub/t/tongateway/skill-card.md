## Description: <br>
Tongateway gives agents TON blockchain tools for wallet information, transfers, jettons, NFTs, .ton DNS resolution, prices, DEX orders, and autonomous agent wallets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pewpewgogo](https://clawhub.ai/user/pewpewgogo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent users use Tongateway to connect an MCP-capable agent to TON wallet, lookup, transfer, DEX, and agent-wallet workflows. The skill is intended for wallet-aware blockchain operations where users approve normal transfers and explicitly opt into autonomous agent wallets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent wallet access can remain available through local token and wallet files after authentication. <br>
Mitigation: Protect or delete ~/.tongateway/token and ~/.tongateway/wallets.json when finished, and revoke the session token from the dashboard when access is no longer needed. <br>
Risk: Autonomous agent wallets can spend funds without per-transfer approval once funded and deployed. <br>
Mitigation: Prefer approval-gated safe mode for normal transfers, use autonomous wallets only when explicitly intended, and fund them only with amounts the user is prepared to lose. <br>
Risk: Installing and running the MCP package delegates local execution to a package fetched through npx. <br>
Mitigation: Pin or build the MCP package from source before trusting it with wallet authority, and run it in a sandboxed environment when appropriate. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/pewpewgogo/tongateway) <br>
- [Publisher Profile](https://clawhub.ai/user/pewpewgogo) <br>
- [Tongateway Website](https://tongateway.ai) <br>
- [Tongateway API Docs](https://api.tongateway.ai/docs) <br>
- [npm Package @tongateway/mcp](https://www.npmjs.com/package/@tongateway/mcp) <br>
- [Smithery Listing](https://smithery.ai/servers/tongateway/agent) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, API Calls, Guidance] <br>
**Output Format:** [Markdown with inline JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include TON addresses, nanoTON amounts, transfer request IDs, wallet balances, token and NFT lists, DEX order details, and approval status.] <br>

## Skill Version(s): <br>
0.9.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
