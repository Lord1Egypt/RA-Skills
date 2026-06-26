## Description: <br>
SVM helps agents explain Solana architecture and protocol internals, including the SVM execution engine, account model, consensus, transactions, validator economics, data layer, development tooling, and token extensions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xIchigo](https://clawhub.ai/user/0xIchigo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, protocol researchers, and Solana operators use this skill to get cited, source-grounded explanations of Solana protocol behavior and architecture. It is intended for analysis and guidance rather than implementation support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the Helius MCP server as an external tool provider for public Solana and Helius content. <br>
Mitigation: Review the helius-mcp package before enabling it and confirm the MCP tools available to the agent match the expected public content-fetching behavior. <br>
Risk: Protocol proposals such as Alpenglow, BAM, and slashing can be in progress and may be mistaken for shipped behavior. <br>
Mitigation: Label proposals clearly and cite the relevant blog post, SIMD, or source path in substantive answers. <br>


## Reference(s): <br>
- [SVM on ClawHub](https://clawhub.ai/0xIchigo/svm) <br>
- [Account Model & Programming Model](references/accounts.md) <br>
- [Compilation Pipeline](references/compilation.md) <br>
- [Consensus](references/consensus.md) <br>
- [Data Layer](references/data.md) <br>
- [Program Development](references/development.md) <br>
- [Execution Engine](references/execution.md) <br>
- [Program Deployment](references/programs.md) <br>
- [Token Extensions & DeFi Primitives](references/tokens.md) <br>
- [Transactions & Local Fee Markets](references/transactions.md) <br>
- [Validator Economics](references/validators.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown responses with citations to source URLs, SIMDs, or repository paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responds in conversation only and does not write local files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
