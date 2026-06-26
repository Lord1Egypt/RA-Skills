## Description: <br>
Spend Pulse helps an agent sync Plaid-backed card transactions, compare monthly spending against a budget, and generate pace-based spending alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jbornhorst1524](https://clawhub.ai/user/jbornhorst1524) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Individuals and agents use this skill to monitor credit card spending, decide when a spending update is warranted, and compose short private alerts with optional chart attachments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects to Plaid-backed financial accounts and processes sensitive spending data. <br>
Mitigation: Install only for trusted private use, connect only accounts the user intends to monitor, and avoid sharing generated summaries or charts outside private contexts. <br>
Risk: Alerts and charts can expose recent merchants, account context, budgets, and spending pace. <br>
Mitigation: Review message content and chart attachments before sending them, especially in shared chats or public channels. <br>
Risk: Spending decisions may be based on stale data if transactions have not been synced recently. <br>
Mitigation: Run a fresh sync before relying on status, check, or chart output for timely budget decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jbornhorst1524/spend-pulse) <br>
- [Plaid developer keys](https://dashboard.plaid.com/developers/keys) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [YAML-style text summaries, concise Markdown prose, shell command guidance, configuration values, and PNG chart file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include sensitive spending totals, transaction snippets, alert decisions, and local chart paths.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
