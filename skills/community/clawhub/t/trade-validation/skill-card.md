## Description:

Trade Validation provides a 10-dimension weighted scoring framework for evaluating prediction-market trades with position sizing, circuit breakers, and mandatory counter-arguments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[staybased](https://clawhub.ai/user/staybased)

### License/Terms of Use:


## Use Case:

External users and agents use this skill as a prediction-market pre-trade checklist to score Polymarket or Kalshi opportunities, compare outcomes, decide position sizes, and document counter-arguments before any trade decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may influence financial decisions if its score is treated as approval to trade.

Mitigation: Treat it as a decision-support checklist only, verify market data and sources independently, and keep final trade approval manual.

Risk: Account-connected automation could turn checklist output into unintended trade execution.

Mitigation: Do not pair the skill with tools that can place trades unless every trade requires explicit confirmation.

Risk: Prediction-market inputs can be incomplete, stale, or overconfident.

Mitigation: Use the required independent-source checks, mandatory counter-argument, veto rules, liquidity threshold, and exposure limits before acting.

## Reference(s):

- [Scoring Rubric](references/scoring-rubric.md)
- [ClawHub Skill Page](https://clawhub.ai/staybased/skills/trade-validation)
- [Publisher Profile](https://clawhub.ai/user/staybased)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown checklist and scoring guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces weighted scores, pass/fail or veto decisions, position-size guidance, counter-argument prompts, and trade-journal entries.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter: 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
