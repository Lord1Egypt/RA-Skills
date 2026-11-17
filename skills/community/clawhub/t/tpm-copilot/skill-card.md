## Description:

TPM Copilot helps Technical Program Managers and Project Managers generate status reports, track risks and blockers, prepare meetings, map dependencies, and create stakeholder dashboards from Jira, Linear, GitHub, and calendar data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[reighlan](https://clawhub.ai/user/reighlan)

### License/Terms of Use:


## Use Case:

Technical Program Managers, Project Managers, and engineering leaders use this skill to synthesize project system data into program status, risk, meeting, dependency, and dashboard outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles service credentials and configurable endpoints for Jira, Linear, GitHub, Slack, and email workflows.

Mitigation: Store tokens outside committed configuration files, restrict configuration file permissions, and use least-privileged service tokens.

Risk: The skill can send project data to configured report delivery or alert destinations.

Mitigation: Validate Jira, webhook, Slack, and email destinations and review generated content before ticket creation or external delivery.

## Reference(s):

- [Jira API Setup](references/jira-setup.md)
- [Linear API Setup](references/linear-setup.md)
- [Report Templates & Customization](references/report-templates.md)
- [Risk Categories & Severity](references/risk-categories.md)
- [Atlassian API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
- [Linear GraphQL API](https://api.linear.app/graphql)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, terminal summaries, JSON workspace records, and shell command guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write local TPM workspace files and can send reports or alerts to configured Slack and email destinations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
