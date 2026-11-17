## Description:

Places GTC bid and ask limit orders on liquid Polymarket markets by selecting active markets and quoting around the CLOB midpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[prysm96](https://clawhub.ai/user/prysm96)

### License/Terms of Use:

MIT-0

## Use Case:

External traders and developers use this skill to run or evaluate a configurable Polymarket market-making strategy that selects liquid markets, quotes around the CLOB midpoint, and can execute in dry-run or live mode.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can cancel all open account orders before placing market-making quotes.

Mitigation: Use paper mode first, prefer a dedicated restricted API key or isolated account, and avoid --live when unrelated orders are open.

Risk: The skill requires trading credentials and uses simmer-sdk to access trading functionality.

Mitigation: Pin or verify simmer-sdk before installation and provide credentials scoped only to the intended trading account.

Risk: Automated market making can place real-money GTC orders based on live market data and local configuration.

Mitigation: Keep conservative limits for maximum order size and market count, review configuration before live runs, and monitor positions after execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/prysm96/skills/simmer-market-maker)
- [Polymarket CLOB endpoint](https://clob.polymarket.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [CLI text output with optional JSON automaton status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY and simmer-sdk; default run is dry-run, while --live can place real orders.]

## Skill Version(s):

1.3.0 (source: server release metadata; artifact frontmatter reports 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
