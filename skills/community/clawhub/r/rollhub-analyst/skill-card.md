## Description:

Research and backtest gambling strategies on a provably fair crypto casino, including Martingale, Kelly Criterion, D'Alembert, Anti-Martingale, and Flat Bet strategies with statistical analysis and reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rollhub-dev](https://clawhub.ai/user/rollhub-dev)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to study gambling strategy outcomes, run casino API-backed micro-bet sessions, calculate bankroll and variance metrics, and prepare markdown strategy comparison reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled script can place repeated live casino bets with an API key and has no built-in spend limit or per-bet confirmation.

Mitigation: Use only sandbox or externally capped accounts, set strict account-level limits before execution, and require human approval for any live-wager run.

Risk: Generated reports may state that bets were verified even though independent verification is not enforced by the bundled runner.

Mitigation: Independently verify each bet through the service verification endpoint and retain those results before making any provably fair verification claim.

Risk: The API key enables account actions against the casino service.

Mitigation: Store the key outside prompts and source files, scope it to the minimum account needed, and rotate or revoke it after testing.

## Reference(s):

- [Gambling Strategies - Detailed Math](references/strategies.md)
- [Strategy Analysis Report Template](references/report-template.md)
- [Agent Casino API](https://agent.rollhub.com/api/v1)
- [ClawHub Skill Page](https://clawhub.ai/rollhub-dev/skills/rollhub-analyst)
- [ClawHub Publisher Profile](https://clawhub.ai/user/rollhub-dev)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and report templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate live casino API requests when users run the bundled shell script with an API key.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
