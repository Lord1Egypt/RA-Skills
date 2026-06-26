## Description: <br>
Private web tools for AI agents: search, scrape, and screenshot the web with x402 micropayments using USDC on Base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kodos-vibe](https://clawhub.ai/user/kodos-vibe) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to let an agent search, scrape, and capture screenshots through an x402-paid gateway for tasks where per-request web access is acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet-backed auto-payment can spend funds on unintended or excessive requests. <br>
Mitigation: Use a dedicated low-balance wallet, review each paid request, and keep only small USDC and ETH balances available. <br>
Risk: Private keys can leak through chat, shell history, logs, environment captures, or shared files. <br>
Mitigation: Use a restricted key file with tight permissions and avoid pasting private keys into chat, commands, logs, or shared documents. <br>
Risk: Broad web-fetch and screenshot authority can send secrets, internal URLs, authenticated pages, or regulated data to the gateway. <br>
Mitigation: Do not submit sensitive, internal, authenticated, or regulated content unless the gateway's privacy and retention practices are acceptable for that use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kodos-vibe/x402-private-web-tools) <br>
- [x402 Private Web Tools service reference](artifact/references/services.md) <br>
- [x402 gateway](https://search.reversesandbox.com) <br>
- [x402 tools MCP repository](https://github.com/kodos-vibe/x402-tools-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, images] <br>
**Output Format:** [Markdown/text scraping results, JSON search responses, PNG/JPEG screenshots, and shell command guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Paid requests require an EVM wallet funded with USDC and ETH on Base; screenshots may be saved as binary image files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
