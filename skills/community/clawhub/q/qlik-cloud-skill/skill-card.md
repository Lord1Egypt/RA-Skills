## Description:

Qlik Cloud provides an agent with Qlik Cloud analytics operations across health checks, search, app management, reloads, Insight Advisor queries, automations, AutoML, Qlik Answers, alerts, spaces, users, licenses, data files, and lineage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[undsoul](https://clawhub.ai/user/undsoul)

### License/Terms of Use:


## Use Case:

Developers, analysts, and operations teams use this skill to manage and inspect Qlik Cloud tenants, apps, reloads, automations, alerts, AI assistants, and analytics data from an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Qlik API key and its documentation suggests storing it in a Markdown file, which can expose tenant credentials.

Mitigation: Use a least-privilege Qlik API key, provide it through environment variables or a secrets manager, and avoid storing it in shared Markdown files.

Risk: The skill lists tenant-changing operations including deletion, reloads, automation runs, and alert evaluations.

Mitigation: Require explicit user confirmation and verify target IDs before running destructive or tenant-changing commands.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with bash commands; Qlik scripts return JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires QLIK_TENANT and QLIK_API_KEY environment variables.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
