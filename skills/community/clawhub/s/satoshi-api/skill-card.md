## Description: <br>
Bitcoin intelligence: fee recommendations, mempool status, price, block info, and address lookups via the Satoshi API. Zero config — no node required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Bortlesboat](https://clawhub.ai/user/Bortlesboat) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to query Bitcoin fee recommendations, mempool status, price, latest block details, address balances, and halving information without running a Bitcoin node. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Address lookups disclose the queried Bitcoin address to bitcoinsapi.com along with normal request metadata. <br>
Mitigation: Avoid querying addresses that are private or sensitive unless sharing them with the external data provider is acceptable. <br>
Risk: Network calls to bitcoinsapi.com may return unavailable, delayed, or provider-specific Bitcoin data. <br>
Mitigation: Treat results as external API data and verify high-value transaction decisions against an independent source before acting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Bortlesboat/satoshi-api) <br>
- [Bortlesboat publisher profile](https://clawhub.ai/user/Bortlesboat) <br>
- [Satoshi API](https://bitcoinsapi.com) <br>
- [Satoshi API v1 endpoint](https://bitcoinsapi.com/api/v1) <br>
- [Related bitcoin-mcp project](https://github.com/Bortlesboat/bitcoin-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-formatted command output and concise text summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv and Python 3.10 or newer; calls bitcoinsapi.com over the network.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
