## Description: <br>
Analyze Venus Protocol lending/borrowing positions on BNB Chain with risk-first guidance. Use when users ask about Venus markets, collateral/borrow decisions, health factor, liquidation risk, APY/utilization comparison, isolated pools, or "can I borrow X safely" style what-if checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zed-venus](https://clawhub.ai/user/zed-venus) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and DeFi operators use this skill to inspect Venus and Flux market data, evaluate wallet health, simulate borrow or withdrawal scenarios, and prepare cautious execution plans for BNB Chain lending operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes scripts that can broadcast real DeFi transactions and request private keys for command-line execution. <br>
Mitigation: Use simulation mode by default, avoid pasting real private keys into shell commands, prefer a safer wallet signer or low-balance test wallet, and require explicit review before any broadcast command. <br>
Risk: Borrowing, withdrawing, collateral changes, and force-risk commands can create liquidation exposure or irreversible asset loss. <br>
Mitigation: Run health-factor simulations first, keep conservative buffers above the documented safety line, start with small amounts, and treat force-risk options as exceptional manual overrides. <br>
Risk: Market data, onchain reads, RPC responses, and API availability can be stale, incomplete, or temporarily unavailable. <br>
Mitigation: State data freshness and assumptions in outputs, cross-check critical values before execution, and avoid claiming guaranteed safety or returns. <br>


## Reference(s): <br>
- [Venus Protocol overview](references/protocol-overview.md) <br>
- [Risk rules](references/risk-rules.md) <br>
- [BNB Chain contract notes](references/bnbchain-contracts.md) <br>
- [Venus quick commands](references/quick-commands.md) <br>
- [Flux quick commands](references/flux-quick-commands.md) <br>
- [Flux BNB addresses](references/flux-bnb-addresses.json) <br>
- [Skill summary](references/skill-summary.md) <br>
- [Venus API](https://api.venus.io) <br>
- [Instadapp Fluid BNB deployments](https://github.com/Instadapp/fluid-contracts-public/tree/main/deployments/bnb) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with inline shell commands and JSON output from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs emphasize risk status, current metrics, safe ranges, recommended actions, and assumptions.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
