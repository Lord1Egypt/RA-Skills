## Description:

Provides Chinese-language guidance about the qintianjian website, cyclical economic theories, Jupiter-cycle mappings, QCX/BTC sentiment, and multi-year crypto and economic timing prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dapp20260215-lab](https://clawhub.ai/user/dapp20260215-lab)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to answer questions about the qintianjian project, its cycle-based economic framework, QCX scoring, BTC sentiment mapping, and stated 20-year warning timeline. The skill is best treated as explanatory and speculative market commentary, not personalized financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake speculative crypto and investment-timing commentary for personalized financial advice.

Mitigation: Present cycle scores, BTC sentiment mapping, and forecasts as speculative commentary only, and do not use them as the sole basis for trading or investment decisions.

Risk: Directive phrases in the artifact encourage risk-on or risk-off actions without clear risk limits.

Mitigation: Add clear financial-advice disclaimers, require independent validation, and avoid personalized recommendations unless reviewed by qualified professionals.

Risk: External BTC sentiment lookup could expose private context if implementation sends user-specific data with the request.

Mitigation: Use only the public Alternative.me endpoint for sentiment data and do not send private user context to that API.

Risk: Multi-year cycle forecasts may overstate certainty.

Mitigation: Label forecasts as unverified heuristic projections and pair them with current, independently sourced market and policy context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dapp20260215-lab/skills/qintianjian)
- [qintianjian website](https://qintianjian.fun/)
- [qintianjian DAPP](https://dapp.qintianjian.fun/)
- [Alternative.me Fear and Greed API](https://api.alternative.me/fng/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, API calls]

**Output Format:** [Markdown text with command-style responses, tables, and short explanatory guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May incorporate public BTC sentiment data from Alternative.me; private user context should not be sent to that API.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
