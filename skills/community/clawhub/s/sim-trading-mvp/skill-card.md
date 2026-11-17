## Description:

Run a disciplined paper-trading workflow with style selection, risk rules, daily decision windows, optional cron automation, persistent account logs, and truthful post-market recaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qrg-cloud](https://clawhub.ai/user/qrg-cloud)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to run and maintain a simulated US stock and ETF trading account with repeatable buy, sell, or hold decisions. Agents use it to set up local paper-account files, evaluate market context, enforce risk rules, record decisions, and produce concise post-market recaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can create or update persistent local paper-account state and trade logs.

Mitigation: Confirm the project path with the user and read existing account and trade-log files before making decisions or updates.

Risk: Optional cron automation can create recurring trading-decision and post-market jobs.

Mitigation: Confirm that the user wants automation, inspect existing cron jobs first, and avoid duplicate scheduled jobs.

Risk: Market-data API keys could be mishandled if placed in public skill files or echoed in reports.

Mitigation: Keep API keys in local runtime configuration only and never publish, commit, or display them in skill artifacts.

Risk: Account valuation can be misleading when position prices are missing.

Mitigation: Label missing or incomplete market data clearly, prefer HOLD when data is unavailable, and avoid relying on valuation until missing-price handling is fixed.

Risk: Users may mistake the workflow for real-money trading support.

Mitigation: Present the workflow as simulated paper trading and confirm the user wants a simulated, not real-money, account.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/qrg-cloud/skills/sim-trading-mvp)
- [Project Template](references/project-template.md)
- [Report Template](references/report-template.md)
- [Trading Log Schema](references/log-schema.md)
- [Cron Setup](references/cron-setup.md)
- [Style Profiles](references/style-profiles.md)
- [Project Notes](references/project-notes.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON account state, JSONL trade log records, shell commands, and local configuration instructions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local paper-account files, append trade-log records, propose cron jobs, and produce a concise Chinese post-market recap.]

## Skill Version(s):

0.2.1 (source: ClawHub server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
