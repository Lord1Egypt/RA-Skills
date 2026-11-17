## Description:

Guides agents in explaining, implementing, or debugging TqSdk Python workflows for update loops, market data, historical downloads, account selection, trading, simulation, backtesting, and common errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shinny-xuyida](https://clawhub.ai/user/shinny-xuyida)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading-system builders use this skill to answer TqSdk questions, produce focused Python examples, choose account modes, and troubleshoot data, order, simulation, and backtest behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples may be adapted into code that places or cancels real orders.

Mitigation: Use simulation or backtest first, confirm the intended account type, and review any order code before running it against a live brokerage account.

Risk: Brokerage or Quick credentials could be copied into source files while testing examples.

Mitigation: Keep real credentials out of source files and use local secret handling for any TqAuth or brokerage account values.

## Reference(s):

- [Account Type Matrix](references/account-type-matrix.md)
- [Accounts And Trading](references/accounts-and-trading.md)
- [Error FAQ](references/error-faq.md)
- [Example Map](references/example-map.md)
- [Market Data](references/market-data.md)
- [Object Fields](references/object-fields.md)
- [Order Functions And Position Tools](references/order-functions-and-position-tools.md)
- [Simulation And Backtest](references/simulation-and-backtest.md)
- [wait_update And The Update Loop](references/wait-update-and-update-loop.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with concise explanations and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers should distinguish futures and stock workflows, choose the account mode explicitly, and identify live-order risks before code is used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
