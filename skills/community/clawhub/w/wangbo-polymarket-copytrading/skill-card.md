## Description: <br>
Build and run Polymarket copy-trading workflows for trader discovery, peak and decline cycle detection, candidate ranking, risk limits, and execution handoff. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangbo12bob2-source](https://clawhub.ai/user/wangbo12bob2-source) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to identify Polymarket traders to copy, assess leaderboard consistency and phase signals, produce risk-limited copy-trade plans, and optionally hand approved rules to execution scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place unattended live Polymarket orders when execution mode is enabled. <br>
Mitigation: Start with the scan script and dry-run mode, verify the active account and config, and only enable execution with external spending limits, duplicate-order controls, monitoring, and a clear stop procedure. <br>
Risk: Configured copy-trade rules may trade the wrong market, outcome, wallet, amount, or threshold. <br>
Mitigation: Review every rule in the JSON config before use, keep position sizes small, cap concurrent positions, and confirm market availability and entry price before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangbo12bob2-source/wangbo-polymarket-copytrading) <br>
- [Publisher profile](https://clawhub.ai/user/wangbo12bob2-source) <br>
- [Polymarket leaderboard Data API](https://data-api.polymarket.com/v1/leaderboard) <br>
- [Auto copytrade config example](references/auto-copytrade-config.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JSON configuration examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce trader rankings, wallet identifiers, risk limits, dry-run commands, and execution handoff steps.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
