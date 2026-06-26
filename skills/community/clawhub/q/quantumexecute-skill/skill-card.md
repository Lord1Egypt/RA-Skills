## Description: <br>
Crypto Algo Execution & TCA by QuantumExecute (QE) supports crypto algorithmic execution workflows across Binance, OKX, LTP, Deribit, Hyperliquid, and other supported exchanges, with TWAP/VWAP/POV tools for order execution, balances, positions, lifecycle control, and TCA reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[l-kai890](https://clawhub.ai/user/l-kai890) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and trading operations teams use this skill to inspect crypto exchange account state, prepare and manage QuantumExecute algorithmic orders, and review execution quality through TCA reports. It is intended for credentialed QuantumExecute accounts with exchange API bindings already configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated trading scripts can create, update, or cancel live orders through QuantumExecute and bound exchange accounts. <br>
Mitigation: Require explicit confirmation for create, update, and cancel operations, review final parameters before execution, use restricted API keys, disable withdrawals, and apply exchange IP allowlists where available. <br>
Risk: Notification workflows can send order details to webhook destinations or execute a configured local command. <br>
Mitigation: Use webhook notifications only with trusted destinations, avoid the command notification channel unless the executable path and environment are fully controlled, and prefer direct status queries in hosted agents. <br>
Risk: Excel exports may contain trading history, fills, balances, positions, or other account-related data. <br>
Mitigation: Write reports only to trusted local folders and delete exported files when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/l-kai890/quantumexecute-skill) <br>
- [QuantumExecute Homepage](https://www.quantumexecute.com/) <br>
- [QuantumExecute API Docs](https://api.quantumexecute.com/trading-api) <br>
- [Safety Reference](references/safety.md) <br>
- [Trading Reference](references/trading.md) <br>
- [Balance Reference](references/balance.md) <br>
- [Tools Reference](references/tools.md) <br>
- [Output Formats Reference](references/output-formats.md) <br>
- [Error and Anti-Fabrication Reference](references/errors.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown and plain text with JSON script outputs, shell commands, and generated Excel report files when export scripts are used] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Authenticated workflows require QE_API_KEY and QE_API_SECRET environment variables; generated reports may be written under QE_WORKSPACE or the local workspace.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter reports 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
