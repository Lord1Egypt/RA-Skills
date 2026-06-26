## Description: <br>
Make x402 payments. Pay for APIs, sell your services, handle 402 Payment Required responses with USDC on Base and other EVM chains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[primer-dev](https://clawhub.ai/user/primer-dev) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use xClaw02 to inspect and satisfy x402 payment requests, make USDC payments for paid APIs, manage wallet setup and balances, and add x402 paywalls to their own services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make real x402/USDC payments and sign transactions. <br>
Mitigation: Require explicit user confirmation for the amount, recipient, network, and URL before any payment, and use configured spending limits. <br>
Risk: Wallet private keys or mnemonics could be exposed through chat, logs, or command output. <br>
Mitigation: Use environment variables or local configuration for wallet credentials, never paste secrets into chat, and use a dedicated low-balance wallet. <br>
Risk: Installing or running package commands from npm or PyPI can execute third-party code. <br>
Mitigation: Verify the package source before running npx or pip commands and install only when agent-assisted x402 payments are intended. <br>


## Reference(s): <br>
- [x402 Protocol](https://x402.org) <br>
- [xClaw02 npm package](https://npmjs.com/package/xclaw02) <br>
- [xClaw02 PyPI package](https://pypi.org/project/xclaw02) <br>
- [xClaw02 GitHub repository](https://github.com/primer-systems/xClaw02) <br>
- [xClaw02 ClawHub page](https://clawhub.ai/primer-dev/xclaw02) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose CLI commands, environment variables, wallet operations, payment confirmations, and Node.js or Python integration snippets.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
