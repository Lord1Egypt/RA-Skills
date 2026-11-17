## Description:

Crypto Algo Execution & TCA by QuantumExecute (QE) supports crypto algorithmic execution workflows across Binance, OKX, LTP, Deribit, Hyperliquid, and other supported exchanges, with TWAP, VWAP, POV, order lifecycle, balance and position, and TCA/reporting workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[l-kai890](https://clawhub.ai/user/l-kai890)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading teams can use this skill to operate QuantumExecute crypto execution workflows, inspect balances and positions, manage orders, and generate TCA reports through authenticated scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, update, cancel, and pair live crypto orders through authenticated QuantumExecute APIs.

Mitigation: Install only for users intended to have live crypto-trading authority, use restricted and IP-whitelisted QE/exchange keys, separate read-only from trade-enabled credentials, and require explicit human confirmation before order-write commands.

Risk: Optional notification paths may send private order details to destinations or commands outside the agent session.

Mitigation: Avoid webhook and command notification channels unless the destination or executable is fully controlled and approved.

Risk: Generated Excel reports may contain trading history, fills, balances, positions, or other account-related data.

Mitigation: Write reports only to trusted local folders such as QE_WORKSPACE and delete exported reports when no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/l-kai890/skills/quantumexecute-skill)
- [QuantumExecute homepage](https://www.quantumexecute.com/)
- [QuantumExecute API docs](https://api.quantumexecute.com/trading-api)
- [QuantumExecute Python SDK](https://github.com/Quantum-Execute/qe-connector-python)
- [QuantumExecute Go SDK](https://github.com/Quantum-Execute/qe-connector-go)
- [Trading Reference](references/trading.md)
- [Safety Reference](references/safety.md)
- [Balance Reference](references/balance.md)
- [Tools Reference](references/tools.md)
- [Error and Anti-Fabrication Reference](references/errors.md)
- [Fixed Output Formats](references/output-formats.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown and text with shell command examples, JSON script outputs, and generated Excel report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Order and TCA responses should preserve script output precision and stable field order; Excel exports may be written to QE_WORKSPACE or the local workspace.]

## Skill Version(s):

1.0.3 (source: server release evidence; artifact frontmatter says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
