## Description: <br>
Query blockchain wallet data, token prices, and transaction history using the Zerion API via its MCP connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vshamanov](https://clawhub.ai/user/vshamanov) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and agents use this skill to retrieve Zerion wallet analytics, token prices, DeFi positions, NFT holdings, PnL, and transaction history for web3 analysis and dashboards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary says the skill teaches agents to put a user's API key into prompts sent to an external model service. <br>
Mitigation: Use only a revocable, low-privilege Zerion API key through a trusted connector or secure credential field, avoid embedding it in prompts or generated artifacts, and revoke it if it was pasted into an artifact or sent to a model endpoint. <br>


## Reference(s): <br>
- [Wallet Endpoints Reference](references/wallet-endpoints.md) <br>
- [Fungible & NFT Endpoints Reference](references/fungible-nft-endpoints.md) <br>
- [Zerion MCP Server](https://developers.zerion.io/mcp) <br>
- [Zerion Developer Dashboard](https://dashboard.zerion.io/) <br>
- [ClawHub Skill Page](https://clawhub.ai/vshamanov/zerion-api-skill-2) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Code, Configuration] <br>
**Output Format:** [Markdown guidance with endpoint details, prompt patterns, code snippets, and JSON API or MCP responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided Zerion API key for authenticated requests.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
