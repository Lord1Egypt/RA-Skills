## Description: <br>
Explore Web3 on-chain data using Chainbase APIs for token holders, wallet addresses, token prices, NFTs, ENS domains, transactions, DeFi portfolios, and cross-chain analytics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lxcong](https://clawhub.ai/user/lxcong) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and analysts use this skill to route natural-language Web3 questions to Chainbase API calls or SQL queries and summarize public on-chain data across supported EVM chains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad custom SQL or raw endpoint requests can expose sensitive wallet addresses or query logic to Chainbase. <br>
Mitigation: Review custom SQL, raw endpoint parameters, and wallet identifiers before execution. <br>
Risk: Using a long-lived or overbroad Chainbase API key increases impact if the environment is exposed. <br>
Mitigation: Use a scoped Chainbase API key in CHAINBASE_API_KEY and rotate it according to local credential policy. <br>


## Reference(s): <br>
- [Chainbase](https://chainbase.com) <br>
- [Chainbase Console](https://console.chainbase.com) <br>
- [API Endpoint Reference](references/api-endpoints.md) <br>
- [ClawHub skill page](https://clawhub.ai/lxcong/web3-data) <br>
- [Project homepage](https://github.com/lxcong/web3-data-skill) <br>
- [Support](https://github.com/lxcong/web3-data-skill/issues) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, API parameters, SQL examples, and summarized JSON results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require CHAINBASE_API_KEY for higher rate limits; uses Chainbase demo access by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: clawhub.json and release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
