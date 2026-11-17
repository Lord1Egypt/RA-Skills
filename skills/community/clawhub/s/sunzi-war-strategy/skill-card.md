## Description:

Sunzi War Strategy maps Sun Tzu's Art of War to a six-dimensional A-share stock analysis score and produces Chinese-language diagnostic reports covering trend, momentum, sentiment, position sizing, risk controls, and intelligence checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[141553](https://clawhub.ai/user/141553)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to structure Chinese-language A-share stock reviews, holdings retrospectives, and risk-aware watchlist analysis. It is intended to produce methodology-driven diagnostic reports rather than investment advice or trade execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial-analysis output could be mistaken for investment advice or direct trading instructions.

Mitigation: Treat outputs as research methodology, keep recommendations conditional, and include the skill's disclaimer that A-share investing involves risk.

Risk: Holdings reviews may expose sensitive account information if users provide full exports or brokerage credentials.

Mitigation: Do not provide brokerage credentials or full account exports; share only the holdings fields needed for the requested review.

## Reference(s):

- [Sunzi War Strategy Skill](SKILL.md)
- [Strategies Reference](references/strategies.md)
- [Signals Reference](references/signals.md)
- [Backtest Notes](references/backtest_notes.md)
- [ClawHub Skill Page](https://clawhub.ai/141553/skills/sunzi-war-strategy)
- [Publisher Profile](https://clawhub.ai/user/141553)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown diagnostic report with optional JSON scoring output and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include the skill's investment-risk disclaimer and avoid brokerage credentials, full account exports, or exact trade instructions.]

## Skill Version(s):

1.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
