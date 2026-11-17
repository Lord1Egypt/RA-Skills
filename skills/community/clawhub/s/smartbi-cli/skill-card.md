## Description:

SmartBI CLI helps agents discover and call SmartBI APIs for model and report queries, AI-assisted insight workflows, scheduling, push messaging, resource management, permissions, and related BI operations through @smartbi/cli.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wahsonleung](https://clawhub.ai/user/wahsonleung)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, BI operators, and external agent users use this skill to connect an agent to a SmartBI environment, resolve business resources, query model or report data, and operate supported SmartBI workflows through verified CLI/API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install or rely on a globally available SmartBI CLI package.

Mitigation: Review the npm global installation path and CLI version before use, and install only in environments where the agent is allowed to execute SmartBI commands.

Risk: The skill may persist SmartBI access tokens for later CLI calls.

Mitigation: Prefer environment-variable or system-keyring token storage, avoid exposing literal tokens in command history or logs, and rotate credentials if exposure is suspected.

Risk: The skill can perform broad SmartBI administrative or mutating actions with the user's account permissions.

Mitigation: Require explicit user confirmation before schedules, pushes, workflow changes, provider changes, permission changes, or resource mutations.

## Reference(s):

- [SmartBI CLI Skill README](artifact/README.md)
- [SmartBI CLI Skill Definition](artifact/SKILL.md)
- [Query Routing Reference](artifact/references/query-routing.md)
- [Data Model Query Reference](artifact/references/data-model-query.md)
- [Report Query Reference](artifact/references/report-query.md)
- [Installation and Configuration Reference](artifact/references/init.md)
- [Call Execution Reference](artifact/references/call.md)
- [SmartBI CLI ClawHub Listing](https://clawhub.ai/wahsonleung/skills/smartbi-cli)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON request-body examples, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce SmartBI CLI commands, API request bodies, query results, troubleshooting guidance, and local file handling instructions.]

## Skill Version(s):

2.1.0 (source: server release evidence and artifact README)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
