## Description: <br>
Research and backtest gambling strategies on a provably fair crypto casino using real micro-bets, statistical metrics, and Rollhub API verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rollhub-dev](https://clawhub.ai/user/rollhub-dev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and analysts use this skill to run and compare gambling strategy backtests against Rollhub casino outcomes and produce risk and return reports. It should be used only by users who intentionally want agent-assisted analysis connected to a Rollhub gambling account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The included script can automatically place real casino bets with a user's API key. <br>
Mitigation: Use a sandbox or offline simulation when possible, and do not run it against a funded account unless strict round, wager, and loss limits are already set. <br>
Risk: The release evidence reports weak warnings and no spending safeguards. <br>
Mitigation: Review the script before execution, use a low-balance revocable API key, and treat every /bet request as a real wager that can lose money. <br>


## Reference(s): <br>
- [Gambling Strategies - Detailed Math](references/strategies.md) <br>
- [Strategy Analysis Report Template](references/report-template.md) <br>
- [Agent Casino API](https://agent.rollhub.com/api/v1) <br>
- [ClawHub Skill Page](https://clawhub.ai/rollhub-dev/rollhub-analyst) <br>
- [Publisher Profile](https://clawhub.ai/user/rollhub-dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown reports with inline shell commands and strategy statistics] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call the Rollhub API and can place live wagers when run with AGENT_CASINO_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
