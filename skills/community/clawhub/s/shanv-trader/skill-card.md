## Description:

Provides AI-assisted semi-automatic stock trading with signal scanning, trade confirmation, risk control, execution, and position monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clementgu](https://clawhub.ai/user/clementgu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading-workflow operators use the skill to scan stock signals, generate human-reviewable trade suggestions, execute selected trades, and monitor positions with alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Executable trading paths can bypass the confirmation and risk-control behavior described in the skill documentation.

Mitigation: Require explicit user confirmation and enforce risk checks inside the executor before any brokerage or trading-platform action.

Risk: Simulated trade execution can be logged as successful, which may mislead users about real order status.

Mitigation: Clearly separate simulation from live execution and only mark trades successful after verified broker confirmation.

Risk: Trading commands accept stock codes and quantities that require stronger validation before live use.

Mitigation: Validate symbols, quantities, price modes, and account limits before executing or recording any transaction.

Risk: Shell command interpolation appears in position-monitoring behavior.

Mitigation: Remove shell=True interpolation and call subprocesses with argument lists or a vetted command wrapper.

## Reference(s):

- [Shanv Trader on ClawHub](https://clawhub.ai/clementgu/skills/shanv-trader)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown-style trade suggestion cards, console text, JSON logs, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save pending trade suggestions and trade logs as JSON files when its scripts are run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
