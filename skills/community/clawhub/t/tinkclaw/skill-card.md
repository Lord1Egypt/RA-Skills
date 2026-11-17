## Description:

Financial market intelligence from TinkClaw, including BUY/SELL/HOLD trading signals, market regime detection, Signal Market bot competition data, proof-chain verification, and natural-language market analysis across crypto, stocks, forex, and commodities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dieub](https://clawhub.ai/user/dieub)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query TinkClaw market intelligence, inspect bot leaderboard and proof-chain data, and format returned signals or analysis for end users. The skill is intended for informational market analysis, not financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials and user prompts may be sent to an arbitrary destination if TINKCLAW_API_URL is changed.

Mitigation: Leave TINKCLAW_API_URL unset or restrict it to a trusted TinkClaw endpoint, and avoid sharing secrets, account details, or confidential trading strategies in prompts.

Risk: Market outputs could be treated as financial advice.

Mitigation: Present TinkClaw data as informational analysis and include the skill's not-financial-advice disclaimer.

## Reference(s):

- [TinkClaw Documentation](https://tinkclaw.com/docs)
- [TinkClaw Signal Market Challenge](https://tinkclaw.com/signal-market/challenge)
- [TinkClaw Skill on ClawHub](https://clawhub.ai/dieub/skills/tinkclaw)
- [TinkClaw Signal Market API Reference](references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and plain-text API results from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include the source attribution and not-financial-advice disclaimer described by the skill.]

## Skill Version(s):

1.2.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
