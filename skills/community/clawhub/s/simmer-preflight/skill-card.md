## Description: <br>
Pre-trade readiness check for autonomous agents. One call returns wallet identity, venue status, spendable balance, open exposure, and a structured ok_to_trade verdict. Run before every real-money trade to prevent cap overruns and catch config issues before they become P&L issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simmer](https://clawhub.ai/user/simmer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and autonomous trading agents use this skill before trade execution to check wallet identity, venue status, spendable balance, open exposure, and risk blockers. It is intended to prevent cap overruns and configuration mistakes before real-money orders are submitted. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Simmer API key and can expose wallet identity, balances, positions, and risk alerts in local agent output. <br>
Mitigation: Install only when connecting a Simmer account is intended, keep SIMMER_API_KEY scoped and secret, and avoid sharing logs or JSON output that contain trading readiness data. <br>
Risk: The preflight verdict is read-only but is designed to inform real-money trading decisions. <br>
Mitigation: Run it once per trade intent, review blockers and warnings before order submission, and keep exposure caps configured for the account's risk limits. <br>


## Reference(s): <br>
- [Simmer API and preflight documentation](https://docs.simmer.markets) <br>
- [Simmer skill page](https://clawhub.ai/simmer/simmer-preflight) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Human-readable CLI summary or structured JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY and may include wallet identity, balances, positions, blockers, warnings, and risk alerts in local agent output.] <br>

## Skill Version(s): <br>
0.3.1 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
