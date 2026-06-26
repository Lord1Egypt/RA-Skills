## Description: <br>
Monte Carlo Crypto Trading Core simulates thousands of future price paths using Geometric Brownian Motion to evaluate win probabilities, risk of ruin, and stop-loss impact for trading strategies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[totoxu](https://clawhub.ai/user/totoxu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to run Monte Carlo simulations for crypto trading scenarios, estimate stop-loss and take-profit probabilities, and summarize risk metrics. Treat the output as educational risk analysis rather than financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts SkillPay during normal use and uses a user ID for billing. <br>
Mitigation: Install only when users are comfortable with SkillPay billing behavior and clearly present any payment URL returned by the skill. <br>
Risk: The billing setup includes unclear bundled default credentials and an unrelated default skill ID. <br>
Mitigation: Configure SKILL_BILLING_API_KEY and SKILL_ID explicitly before use; do not rely on bundled defaults. <br>
Risk: Trading probability outputs can be mistaken for financial advice. <br>
Mitigation: Present results as educational risk analysis and require independent review before making trading decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/totoxu/totoxu-montecarlo) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON simulation results with agent-facing text or markdown summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user billing identifier, current price, and daily volatility; supports optional drift, simulation horizon, path count, position type, stop-loss, and take-profit levels.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
