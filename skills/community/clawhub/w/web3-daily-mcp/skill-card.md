## Description: <br>
MCP Server for Web3 Daily - Real-time Web3 research digest with macro news, KOL sentiment, market data, and personalized wallet analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexander10011](https://clawhub.ai/user/alexander10011) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external users use this MCP server to let compatible agents retrieve Web3 daily digests, market overviews, and optional wallet-based profile analysis in Chinese or English. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Personalized digest and wallet profile tools send wallet addresses to the disclosed J4Y backend for analysis and 24-hour profile caching. <br>
Mitigation: Use public digest and market overview tools when wallet sharing is not acceptable; use personalized tools only for wallet addresses the user is comfortable having profiled and cached for 24 hours. <br>
Risk: The MCP server depends on an external backend service for digests, market data, and wallet analysis. <br>
Mitigation: Treat returned market and wallet analysis as service-provided research output and verify important financial or operational decisions against independent sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alexander10011/web3-daily-mcp) <br>
- [J4Y Backend API](https://j4y-production.up.railway.app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [MCP text responses, with wallet profiles formatted as Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tool inputs include optional language selection and, for personalized features, an EVM wallet address.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence, package.json, claw.json, and MCP server metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
