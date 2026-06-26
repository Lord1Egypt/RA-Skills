## Description: <br>
Run a paper-trading / simulated investing workflow with explicit style selection, fixed risk rules, three decision windows per trading day, optional cron setup, persistent account and trade logs, and a post-market daily recap. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[QRG-cloud](https://clawhub.ai/user/QRG-cloud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to run a disciplined simulated US stock and ETF trading account, make buy/sell/hold decisions during defined market windows, maintain account and trade logs, and produce concise post-market recaps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent scheduled jobs can continue running trading-decision windows after setup. <br>
Mitigation: Confirm automation is intentional, inspect existing cron entries first, use predictable job names, and document how to disable or replace the jobs. <br>
Risk: The skill can modify ongoing account state and append trade-log records. <br>
Mitigation: Confirm the project path and files before setup, review account and log changes, and keep trade records append-only where possible. <br>
Risk: Simulated buy, sell, or hold decisions could be mistaken for financial advice. <br>
Mitigation: Label the workflow as paper trading, keep decisions grounded in retrieved data, prefer HOLD when data is missing, and remind users not to treat simulated decisions as financial advice. <br>
Risk: Market-data API keys may be needed for robust pricing and benchmark handling. <br>
Mitigation: Store keys only in local runtime configuration such as a project .env file, and never publish, commit, hardcode, or echo user secrets. <br>


## Reference(s): <br>
- [Sim Trading MVP on ClawHub](https://clawhub.ai/QRG-cloud/sim-trading-mvp) <br>
- [Cron setup](references/cron-setup.md) <br>
- [Trading log schema](references/log-schema.md) <br>
- [Project notes](references/project-notes.md) <br>
- [Project template](references/project-template.md) <br>
- [Post-market report template](references/report-template.md) <br>
- [Style profiles](references/style-profiles.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON/JSONL records, shell command examples, and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local account state, append trade-log entries, and propose cron automation when the user opts in.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
