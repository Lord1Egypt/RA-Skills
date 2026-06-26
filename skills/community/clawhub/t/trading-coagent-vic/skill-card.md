## Description: <br>
Helps an AI agent monitor trading signals alongside automation scripts, analyze missed or failed trades, document remediation steps, and support supervised crypto or stock trading workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chungvic](https://clawhub.ai/user/chungvic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading-automation operators use this skill to coordinate agent review of crypto and stock trading signals, compare agent findings against script behavior, and plan remediation for missed, failed, or incorrect trades. It is intended for supervised trading automation where live execution access is tightly controlled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed for AI-assisted live trading and discusses agent-initiated trades, retries, and remediation of erroneous trades. <br>
Mitigation: Keep the agent in read-only or paper-trading mode by default, require explicit user confirmation for live orders and retries, and provide a clear stop control before granting live trading access. <br>
Risk: Broad trading access could expose real accounts to unintended losses. <br>
Mitigation: Use tightly scoped trading-only API keys with withdrawals disabled, and enforce hard limits for assets, accounts, position size, per-trade loss, daily loss, and daily trade count. <br>
Risk: Retrying or remediating failed trades can compound losses when market conditions, gas, slippage, RPC behavior, or token details change. <br>
Mitigation: Require fresh signal quality checks, parameter validation, gas and slippage review, and account-balance checks before each retry or corrective trade. <br>


## Reference(s): <br>
- [Trading Checklist](references/trading-checklist.md) <br>
- [Failure Analysis Guide](references/failure-analysis.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/chungvic/trading-coagent-vic) <br>
- [Publisher Profile](https://clawhub.ai/user/chungvic) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, checklists, Python script output, and JSON/JSONL logging conventions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled monitor script reads optional JSON configuration and writes monitoring_log.jsonl entries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
