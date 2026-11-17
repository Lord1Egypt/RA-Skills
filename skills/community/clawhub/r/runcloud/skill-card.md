## Description:

Query Runcloud servers, databases, web apps, services, cronjobs, deployments, and health via the Runcloud API v3.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neshable](https://clawhub.ai/user/neshable)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect and manage Runcloud-hosted infrastructure through documented API calls, including server health, web apps, databases, cron jobs, deployments, services, SSL certificates, and domains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes authenticated POST actions that can affect production infrastructure, including deployments, service restarts, cron job tests, and SSL changes.

Mitigation: Require explicit server, web app, service, or cron identifiers and operator confirmation before running any POST command.

Risk: The Runcloud API token can grant broad workspace access.

Mitigation: Use the least-privilege token available, store it as RUNCLOUD_API_TOKEN, and treat it like a password.

Risk: The security verdict is suspicious because high-impact write actions are framed too lightly.

Mitigation: Review before installing and treat all POST examples as production changes.

## Reference(s):

- [Runcloud API v3 documentation](https://runcloud.io/docs/api/v3/doc-625011)
- [Runcloud API v3 base URL](https://manage.runcloud.io/api/v3)
- [Runcloud Skill on ClawHub](https://clawhub.ai/neshable/skills/runcloud)
- [Publisher profile on ClawHub](https://clawhub.ai/user/neshable)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash and jq command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires jq and RUNCLOUD_API_TOKEN; commands call the Runcloud API with bearer-token authentication.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
