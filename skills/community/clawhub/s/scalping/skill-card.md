## Description:

Generates a high-turnover intraday scalping strategy template for Superior Trade with momentum-burst entries, tight stops, configuration guidance, and validation warnings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superior-ai](https://clawhub.ai/user/superior-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading-strategy authors use this skill to draft and adapt a Superior Trade scalping strategy for fast in/out momentum trades on a 5-minute timeframe. The skill is a structural template and should be backtested, paper-traded, and tuned before any live use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reference strategy is disclosed as unprofitable in its backtest and may create financial losses if used as-is.

Mitigation: Backtest, paper-trade, and tune parameters before live use; treat the output as a strategy template rather than trading advice.

Risk: The configuration uses futures trading and cross margin, which can increase loss exposure.

Mitigation: Review margin, position sizing, stop-loss, and exchange settings carefully before adapting the configuration.

Risk: Tight-target scalping can be materially affected by fees, slippage, and low signal breadth.

Mitigation: Account for fees and slippage in tests and consider broader pair coverage or additional regime filters before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/superior-ai/skills/scalping)

## Skill Output:

**Output Type(s):** [Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with Python and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a reference strategy, configuration requirements, tunable parameters, backtest context, and risk-focused caveats.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
