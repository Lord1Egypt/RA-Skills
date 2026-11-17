## Description:

Read current values from Grafana dashboards by dashboard and panel name without requiring PromQL, SQL, or datasource knowledge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darkstards9](https://clawhub.ai/user/darkstards9)

### License/Terms of Use:


## Use Case:

Developers, operators, and agents use this skill to list Grafana dashboards and panels, then read recent or current metric values already exposed by existing dashboard panels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Grafana credentials can be exposed if the configured Grafana URL uses plain HTTP on an unprotected network.

Mitigation: Configure GRAFANA_URL with HTTPS unless the Grafana instance is strictly local or otherwise protected.

Risk: The skill can read dashboards and datasource-backed panel data available to the configured Grafana account.

Mitigation: Use a dedicated least-privilege Viewer or service account and limit it to dashboards and datasources the agent is authorized to query.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/darkstards9/skills/rpe-grafana)
- [ClawHub publisher profile](https://clawhub.ai/user/darkstards9)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON strings returned as text content, with setup guidance in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool outputs summarize dashboard UIDs, panel IDs, panel titles, last values, units, and Grafana query result names.]

## Skill Version(s):

1.0.2 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
