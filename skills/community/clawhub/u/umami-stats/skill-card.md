## Description:

Query Umami Cloud (v2) analytics data via API using an environment-provided API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hfichter](https://clawhub.ai/user/hfichter)

### License/Terms of Use:


## Use Case:

Developers, operators, and marketing analysts use this skill to fetch read-only Umami analytics data for website traffic, pages, events, sessions, realtime metrics, reports, attribution, planning, experiments, and monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send an Umami API key to a user-configurable API URL, including self-hosted deployments.

Mitigation: Use a least-privileged read-only Umami key, keep cloud mode pointed at https://api.umami.is, use HTTPS for self-hosted deployments, and avoid passing the API key on the command line.

## Reference(s):

- [Umami read endpoints](references/read-endpoints.md)
- [Umami API documentation](https://v2.umami.is/docs/api)

## Skill Output:

**Output Type(s):** [text, markdown, json, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only GET requests using environment-provided Umami configuration and time-range parameters.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
