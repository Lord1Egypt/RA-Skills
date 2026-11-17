## Description:

Generates and modifies Python quantitative trading strategy code for the Guojin PTRADE platform using bundled templates and PTRADE API references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weistiger](https://clawhub.ai/user/weistiger)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and quantitative-trading users use this skill to draft or adapt PTRADE Python strategies, including moving-average, financial-factor, and intraday trading workflows, before review and testing in the PTRADE environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated or bundled PTRADE strategies can place or liquidate real trades when deployed to a live account.

Mitigation: Manually review the strategy, backtest it, paper-trade it, and restrict it to an isolated account or strategy-owned positions before enabling live execution.

Risk: Templates and API references include market orders, margin or futures functions, and fund-transfer capabilities that may exceed a user's intended scope.

Mitigation: Disable or remove fund-transfer, margin, futures, and broad liquidation logic unless the user explicitly requests it and independently verifies the code.

Risk: Generated strategy logic may be incomplete, incorrect, or inconsistent with the active PTRADE API version.

Mitigation: Validate API calls in PTRADE, run `check_strategy` when available, and confirm order sizing, price type, and data access before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weistiger/skills/ptrade-strategy)
- [Publisher profile](https://clawhub.ai/user/weistiger)
- [Knowledge base document index](artifact/kb_ref.md)
- [IMA knowledge base platform](https://ima.qq.com)

## Skill Output:

**Output Type(s):** [Code, Markdown, Guidance, Configuration]

**Output Format:** [Markdown with Python code blocks and concise usage notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated strategies should be reviewed, backtested, and paper-traded before live account use.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
