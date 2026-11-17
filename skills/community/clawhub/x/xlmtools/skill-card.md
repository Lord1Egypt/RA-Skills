## Description:

Live data and actions for Stellar (XLM, Soroban, DEX, USDC), plus crypto prices, stock quotes, weather, domain checks, web search, deep research, screenshots, URL scraping, AI images, and YouTube.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blockchain-oracle](https://clawhub.ai/user/blockchain-oracle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent retrieve current Stellar ecosystem data, market data, weather, domain status, web results, page content, screenshots, generated images, and YouTube information. It also guides agents on paid-tool cost disclosure, confirmation, and transaction reporting for USDC-paid calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned npm install commands can run mutable package code in the agent environment.

Mitigation: Prefer pinned package versions, review the XLMTools npm packages separately, and run them in an isolated sandbox where practical.

Risk: Broad triggers can route general latest, URL, or live-data requests through external tools and paid services.

Mitigation: Review calls before execution, use the cheapest sufficient tool, and avoid paid tools for requests answerable from existing context or training data.

Risk: First run creates a local Stellar testnet wallet configuration and sets up payment-related state automatically.

Mitigation: Install only when that local wallet behavior is acceptable, inspect the generated configuration, and set an MCP budget before paid use.

## Reference(s):

- [ClawHub XLMTools Skill Page](https://clawhub.ai/blockchain-oracle/skills/xlmtools)
- [XLMTools Runtime Manifest](https://api.xlmtools.com/.well-known/xlmtools.json)
- [XLMTools LLM Service Metadata](https://api.xlmtools.com/llms.txt)
- [Circle Testnet USDC Faucet](https://faucet.circle.com)
- [Stellar Lab Testnet Account Funding](https://lab.stellar.org/account/fund)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with inline tool names, shell commands, JSON results, links, costs, and transaction hashes when paid tools are used]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May rely on MCP tools or the xlm CLI; paid calls require cost disclosure, approval for higher-cost tools, and Stellar transaction hash reporting.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
