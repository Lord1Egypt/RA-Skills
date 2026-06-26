## Description: <br>
Upbit automated trading (aggressive breakout) with cron-friendly run-once commands, TopVolume monitoring, and percent-based budget splitting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kuns9](https://clawhub.ai/user/kuns9) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
External users and developers use this skill to run an Upbit trading automation workflow that monitors KRW markets, creates buy and sell events, and processes those events through cron-friendly commands with dry-run support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real Upbit orders when dry-run mode is disabled. <br>
Mitigation: Start with execution.dryRun=true, review budgetPolicy and maxPositions, use minimal funds during testing, and monitor account activity closely. <br>
Risk: Upbit API credentials are required and could be exposed if stored in committed files. <br>
Mitigation: Provide credentials through the OpenClaw secret store or environment variables and avoid storing keys in config.json. <br>
Risk: Automated market monitoring and event processing can act on volatile market signals without human confirmation. <br>
Mitigation: Run smoke_test, monitor_once, and worker_once in dry-run mode first, then review generated events and positions before enabling live trading. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kuns9/trading-upbit-skill) <br>
- [Publisher profile](https://clawhub.ai/user/kuns9) <br>
- [README](artifact/README.md) <br>
- [Security guidance](artifact/SECURITY.md) <br>
- [Upbit API base URL](https://api.upbit.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, JSON files, API calls, guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands and JSON configuration examples; runtime commands emit console logs and JSON resource files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and Upbit API credentials supplied through environment variables or local configuration.] <br>

## Skill Version(s): <br>
1.0.14 (source: ClawHub release metadata; artifact metadata/package.json version: 13.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
