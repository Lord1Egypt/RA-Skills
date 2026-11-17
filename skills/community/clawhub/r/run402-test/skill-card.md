## Description:

Test skill for Run402: provision AI-native Postgres databases with REST API, auth, and row-level security using x402 micropayments on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[majortal](https://clawhub.ai/user/majortal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to provision Run402 Postgres projects, create tables, and query data through REST-backed workflows paid through x402 micropayments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Provisioning workflows may create paid Run402 resources or send x402 payment headers.

Mitigation: Require explicit approval before provisioning projects or sending payment headers; confirm tier, lease, and price first.

Risk: SERVICE_KEY is an admin secret that can authorize arbitrary SQL against a project.

Mitigation: Treat SERVICE_KEY as a high-privilege credential, avoid exposing it in logs, and require approval before running SQL.

Risk: The helper script can read local Run402 credentials from ~/.config/run402/projects.json and submit SQL.

Mitigation: Review or remove sql2.mjs when local credential access is not intended; run it only with an approved project ID and approved SQL.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/majortal/skills/run402-test)
- [Run402 project provisioning API](https://api.run402.com/v1/projects)
- [Run402 admin SQL API](https://api.run402.com/admin/v1/projects/$PROJECT_ID/sql)
- [Run402 REST query API](https://api.run402.com/rest/v1/todos?done=eq.false)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with fenced shell commands, API calls, and JSON field names]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes workflows that may create paid resources, expose service keys, or execute admin SQL and therefore require explicit approval before use.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
