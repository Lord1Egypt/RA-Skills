## Description: <br>
A 10-dimension weighted scoring framework for evaluating prediction-market trades with position-sizing rules, circuit breakers, and required counter-arguments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[staybased](https://clawhub.ai/user/staybased) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to evaluate prediction-market opportunities, compare Polymarket or Kalshi markets, run pre-trade checklists, and document score-based trade decisions. It supports decision review and journaling; it does not execute trades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill records trade journals that may contain financial details. <br>
Mitigation: Keep journals private, avoid syncing or sharing them unintentionally, and remove sensitive financial details before disclosure. <br>
Risk: The scoring framework may be mistaken for a financial guarantee or automated trading safeguard. <br>
Mitigation: Use the output as decision support only, review counter-arguments and risk limits manually, and do not rely on the skill to execute or block trades. <br>


## Reference(s): <br>
- [Scoring Rubric](references/scoring-rubric.md) <br>
- [Trade Validation on ClawHub](https://clawhub.ai/staybased/trade-validation) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Text] <br>
**Output Format:** [Markdown checklists, scoring tables, and trade-journal entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces decision-support guidance only; no credentials, API calls, or trade execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter lists 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
