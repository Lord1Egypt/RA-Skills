## Description: <br>
Pay for x402-enabled Agent endpoints using USDT on TRON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Hades-Ye](https://clawhub.ai/user/Hades-Ye) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to invoke x402-enabled HTTP endpoints that require USDT payments on TRON, including endpoint discovery and paid API requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically use discovered TRON wallet keys and create persistent high-limit USDT approvals. <br>
Mitigation: Use only a dedicated low-balance TRON wallet, start on testnet, and revoke token approvals when they are no longer needed. <br>
Risk: Paid mainnet endpoint invocation can spend funds if an agent calls a payment-required endpoint without review. <br>
Mitigation: Verify the endpoint, network, spender, and price before each use, and require explicit human review before paid mainnet calls. <br>
Risk: Wallet credentials are required for payment signing. <br>
Mitigation: Keep signing secrets out of prompts, logs, and shell commands, and configure credentials only through secure local environment or config mechanisms. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Hades-Ye/x402-payment-tron) <br>
- [x402 homepage](https://x402.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with tool invocation examples and JSON command output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save binary or image responses to temporary files and return file path metadata.] <br>

## Skill Version(s): <br>
0.0.4 (source: server release metadata; artifact frontmatter and package.json report 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
