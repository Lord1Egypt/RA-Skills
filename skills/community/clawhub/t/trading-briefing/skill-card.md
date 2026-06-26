## Description: <br>
Trading Briefing generates a daily cryptocurrency trading report that aggregates market prices, trading bot status, positions and PnL, system health, and strategy discovery status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huiLI203](https://clawhub.ai/user/huiLI203) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers operating an OpenClaw cryptocurrency trading workspace use this skill to inspect market data, bot status, positions, PnL, system health, and strategy discovery status in one report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The report can reveal sensitive local trading status, positions, PnL, recent trade snippets, and system information. <br>
Mitigation: Install and run it only in environments where the agent is allowed to read and display local trading and system status. <br>
Risk: Using --save leaves a Markdown report with trading details on disk. <br>
Mitigation: Use --save only when persistent reports are acceptable, and manage the saved file according to local data-retention and access-control practices. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huiLI203/trading-briefing) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Plain text console report; optional Markdown file when run with --save] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Report may include local trading status, positions, PnL, recent trade snippets, process status, disk usage, and memory usage.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
