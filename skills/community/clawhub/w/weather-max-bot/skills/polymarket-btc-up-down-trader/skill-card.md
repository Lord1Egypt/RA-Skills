## Description: <br>
Trade Polymarket BTC daily and weekly UP/DOWN markets with empirically-anchored exit discipline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simmer](https://clawhub.ai/user/simmer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run or configure an automated Polymarket BTC direction-market strategy for daily and weekly markets. It is intended for disciplined entry, monitoring, and exits, not fast 5-minute or 15-minute markets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place automated real-money Polymarket trades when run in live mode. <br>
Mitigation: Start in dry-run mode, use small budgets, and enable live trading only after reviewing the strategy output and configuration. <br>
Risk: External-wallet use may require sensitive wallet credentials. <br>
Mitigation: Prefer managed wallets when appropriate, or use a dedicated low-balance wallet and keep private keys in environment variables rather than shared files. <br>
Risk: Cron or quiet mode can make repeated trading harder to observe. <br>
Mitigation: Avoid unattended cron and quiet mode until dry-run behavior, budgets, and exit settings have been verified. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/simmer/polymarket-btc-up-down-trader) <br>
- [Publisher profile](https://clawhub.ai/user/simmer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include dry-run output, position summaries, trade status, and configuration guidance when the strategy is executed.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
