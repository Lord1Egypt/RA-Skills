## Description:

Monitors xAI prepaid credit balance with a reusable Python script and alert workflow patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[therealmrb123](https://clawhub.ai/user/therealmrb123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to set up scheduled xAI/Grok prepaid balance checks, low-credit alerts, and optional follow-up task creation without embedding delivery routing in the balance script.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires access to an xAI management key for balance checks.

Mitigation: Provide the key only in the runtime environment, limit access to agents that need balance monitoring, and rotate or revoke it if the environment is shared or compromised.

Risk: Scheduled checks contact the xAI management billing API and alerts may be relied on for account-balance decisions.

Mitigation: Test the JSON output against the target xAI account, choose warning and critical thresholds that match the account's usage rate, and monitor failures as actionable alerts.

Risk: Optional task-creation workflows can create duplicate or misrouted follow-up tasks.

Mitigation: Constrain automation to a specific task list or project and use duplicate-safe task lookup before creating a new task.

## Reference(s):

- [Cron examples](references/cron-examples.md)
- [xAI Management API billing endpoint](https://management-api.x.ai/v1/billing/teams/)
- [ClawHub skill page](https://clawhub.ai/therealmrb123/skills/xai-prepaid-monitor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown guidance with bash commands and normalized JSON script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script reads xAI team and management-key environment variables, applies configurable balance thresholds, and emits a single JSON object for alert automation.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
