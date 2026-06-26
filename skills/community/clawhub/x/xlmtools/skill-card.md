## Description: <br>
XLMTools lets agents retrieve live Stellar/XLM data and broader external data, use Stellar DEX and wallet functions, and call paid search, research, scraping, screenshots, stocks, YouTube, and image tools through MCP or CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blockchain-oracle](https://clawhub.ai/user/blockchain-oracle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agents use this skill to answer requests that require live Stellar, market, web, media, weather, or domain data, and to perform small paid data actions with cost disclosure. It is intended for external data and actions rather than general knowledge, math, coding, or summarizing user-provided text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create persistent local Stellar testnet wallet configuration and make USDC-paid calls. <br>
Mitigation: Install only when that behavior is acceptable, set an MCP budget where possible, and treat ~/.xlmtools/config.json as sensitive local account configuration. <br>
Risk: Some paid tools are designed to run after cost mention rather than explicit approval. <br>
Mitigation: Require explicit approval for every paid call when the agent host supports that policy, especially for research, screenshots, and image generation. <br>
Risk: Broad activation rules may route current-events, URL, or Stellar-related requests through external services. <br>
Mitigation: Use the skill only for requests that need live or external data, and avoid it for general knowledge, math, code, or pasted-text summarization. <br>


## Reference(s): <br>
- [XLMTools ClawHub listing](https://clawhub.ai/blockchain-oracle/xlmtools) <br>
- [XLMTools runtime manifest](https://api.xlmtools.com/.well-known/xlmtools.json) <br>
- [XLMTools llms.txt](https://api.xlmtools.com/llms.txt) <br>
- [Circle testnet USDC faucet](https://faucet.circle.com) <br>
- [Stellar Laboratory account funding](https://lab.stellar.org/account/fund) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON tool results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Paid tool responses can include Stellar testnet payment transaction hashes; MCP responses may be cached for repeated queries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
