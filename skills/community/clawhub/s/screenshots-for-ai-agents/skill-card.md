## Description: <br>
Captures browser screenshots and performs screenshot-based vision analysis for public HTTPS URLs through a Streamable HTTP MCP service with x402 USDC payment for paid tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[buildinhk](https://clawhub.ai/user/buildinhk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to connect agents to a remote MCP service that captures screenshots of public HTTPS pages and can answer vision prompts about those pages. It is suited for public web inspection workflows where the operator accepts off-host processing and x402 USDC payment for paid calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid calls can spend wallet funds or use the wrong advertised payment network. <br>
Mitigation: Check discovery.json before paid calls, confirm the x402 network and current list prices, and use a dedicated low-balance or spending-limited signer. <br>
Risk: Submitted URLs, screenshots, prompts, and vision outputs are processed by the remote provider. <br>
Mitigation: Use the service only for public, non-sensitive HTTPS URLs and avoid internal, authenticated, private, or secret-bearing pages. <br>
Risk: Wallet or signing secrets could be exposed if placed in prompts or page URLs. <br>
Mitigation: Keep signer keys in the agent host environment or vault and never include private keys, tokens, or secrets in prompts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/buildinhk/screenshots-for-ai-agents) <br>
- [Service homepage](https://screenshotx402.com) <br>
- [Machine discovery](https://screenshotx402.com/discovery.json) <br>
- [API reference](https://screenshotx402.com/docs) <br>
- [x402](https://www.x402.org/) <br>
- [Model Context Protocol](https://modelcontextprotocol.io/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance, Images] <br>
**Output Format:** [Markdown guidance and MCP tool results containing image content and optional text analysis.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Paid screenshot and analysis calls require x402 USDC payment proof; health and discovery are free.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
