## Description:

A paper-trading skill that helps an agent create simulated portfolios, place and cancel buy or sell orders, match limit orders, manage market data, calculate NAV, and report portfolio performance metrics with optional Eastmoney price refreshes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevenge791](https://clawhub.ai/user/stevenge791)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to run local paper-trading workflows, including portfolio setup, simulated order placement, order matching, NAV snapshots, and performance review. It is for simulated trading workflows and should not be treated as financial advice or a real brokerage system.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Skill commands persist, change, and can delete local paper-trading portfolio data.

Mitigation: Use a dedicated SIMTRADE_DB_PATH for test data, back up important local databases before use, and review destructive commands such as portfolio or price deletion before execution.

Risk: Default refresh workflows may send holdings symbols to Eastmoney services.

Mitigation: Use --no-refresh when external market-data calls are not wanted, and manually manage cached prices with market_data.py.

Risk: The refresh helper can read EM_API_KEY from the shell profile.

Mitigation: Provide EM_API_KEY explicitly through the process environment and avoid storing sensitive API keys in ~/.bashrc where possible.

Risk: Validation gaps can corrupt simulated trading results.

Mitigation: Review JSON outputs, reconcile portfolio cash and holdings after commands, and avoid relying on generated metrics for real financial decisions.

## Reference(s):

- [Database schema reference](references/schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands mutate a local SQLite paper-trading database and some workflows refresh prices from Eastmoney unless --no-refresh is used.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
