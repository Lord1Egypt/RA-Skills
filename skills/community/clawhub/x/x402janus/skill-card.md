## Description: <br>
x402janus scans EVM wallets for risky approvals, traces fund-flow signals, detects drainer patterns, and builds revoke transactions with x402 USDC payment support on Base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openclaw-consensus-bot](https://clawhub.ai/user/openclaw-consensus-bot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and autonomous-agent operators use this skill as a pre-transaction wallet-security gate to inspect token approvals, receive risk findings, and prepare or execute approval revocations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for wallet-signing authority for paid x402 scans. <br>
Mitigation: Use a dedicated low-balance wallet, review x402 payment terms before signing, and prefer the free tier first. <br>
Risk: The revoke tool can submit real on-chain transactions and can also set nonzero approval allowances. <br>
Mitigation: Use dry-run output by default and do not run --execute or pass --allowance unless the exact transaction is intended. <br>
Risk: A misconfigured JANUS_API_URL could direct requests and payment signing toward an unintended service. <br>
Mitigation: Keep JANUS_API_URL pointed at the intended x402janus service before running paid or transaction-capable commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/openclaw-consensus-bot/x402janus) <br>
- [x402janus product site](https://x402janus.com) <br>
- [GitHub repository](https://github.com/consensus-hq/agent-pulse) <br>
- [Virtuals ACP marketplace listing](https://app.virtuals.io/acp/agent-details/14804) <br>
- [Machine-readable skill documentation endpoint](https://x402janus.com/api/skill-md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and optional JSON scan, approval, monitoring, and transaction outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exit codes indicate safe, medium-risk, high-risk, and critical-risk scan outcomes.] <br>

## Skill Version(s): <br>
3.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
