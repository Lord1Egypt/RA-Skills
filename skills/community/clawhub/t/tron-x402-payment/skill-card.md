## Description: <br>
Pay for x402-enabled Agent endpoints using TRC20 tokens (USDT/USDD) on TRON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wzc1206](https://clawhub.ai/user/wzc1206) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to invoke x402-enabled endpoints and automatically handle TRON TRC20 payment requirements for USDT or USDD requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically use TRON wallet credentials to spend tokens. <br>
Mitigation: Install only when payment behavior is intended, use a dedicated low-balance wallet, and prefer testnet before mainnet use. <br>
Risk: The payment helper may grant long-lived token approvals. <br>
Mitigation: Review target endpoints and prices before use, avoid valuable mainnet keys or ambient mcporter credentials, and revoke token approvals after use. <br>
Risk: Wallet private keys and API keys are sensitive operational secrets. <br>
Mitigation: Use the skill's status check instead of printing environment variables, and keep logs and command history free of signing secrets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wzc1206/tron-x402-payment) <br>
- [x402 protocol](https://x402.org) <br>
- [Publisher profile](https://clawhub.ai/user/wzc1206) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON response details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return API response text or JSON metadata for saved binary/image outputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
