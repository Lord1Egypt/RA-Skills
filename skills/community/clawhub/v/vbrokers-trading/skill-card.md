## Description: <br>
VBrokers Trading helps agents automate VBrokers OpenAPI Gateway workflows for account access, portfolio checks, quotes, orders, cancellations, and stop-loss or take-profit logic across supported US, HK, and A-share markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lcy360](https://clawhub.ai/user/lcy360) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and trading operators use this skill to connect an agent to a local VBrokers OpenAPI Gateway, inspect account state, retrieve quotes and K-lines, and prepare or execute order-management workflows. It is intended for environments where the user intentionally enables agent-assisted brokerage access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent-assisted live trading and cancellation can place unintended brokerage orders if enabled without confirmation or guardrails. <br>
Mitigation: Require explicit per-order approval and validate symbol, quantity, price, session, market status, and account context before calling order or cancellation endpoints. <br>
Risk: Gateway access and trading credentials can expose brokerage account control if mishandled. <br>
Mitigation: Keep the Gateway local, avoid hard-coding real passwords, and begin with read-only quote and account checks before enabling live trading actions. <br>


## Reference(s): <br>
- [VBrokers OpenAPI Reference](references/api-reference.md) <br>
- [VBrokers OpenAPI Documentation](https://quant-open.hstong.com/api-docs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples and JSON API parameter examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local VBrokers OpenAPI Gateway at 127.0.0.1:11111 and pycryptodome for the bundled Python helper.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
