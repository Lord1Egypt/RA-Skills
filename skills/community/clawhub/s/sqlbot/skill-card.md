## Description:

Manage SQLBot workspaces, datasources, ask-data flows, and dashboards, including listing and switching workspace or datasource context, asking questions against a datasource, listing dashboards, viewing dashboard details, and exporting dashboards as JPG/PNG or PDF.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuwei-fit2cloud](https://clawhub.ai/user/xuwei-fit2cloud)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to work with SQLBot from agent-compatible tools: selecting workspaces and datasources, asking data questions, inspecting dashboards, and exporting dashboard views.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dashboard export handles SQLBot authentication broadly in the browser context.

Mitigation: Use dashboard export only with trusted SQLBot origins and isolated networks until authentication headers are scoped to the SQLBot origin.

Risk: The skill requires SQLBot API credentials and reads them from configuration.

Mitigation: Protect the .env file, use least-privilege API keys, and rotate credentials according to local policy.

Risk: The skill can switch SQLBot workspace context, query datasources and chats, read dashboard data, save local context, and write dashboard exports.

Mitigation: Confirm the intended workspace, datasource, dashboard, and output path before running commands that access or export data.

Risk: Dashboard export depends on Playwright and Chromium.

Mitigation: Pin and update Playwright and Chromium in managed environments before enabling export workflows.

## Reference(s):

- [ClawHub SQLBot skill page](https://clawhub.ai/xuwei-fit2cloud/skills/sqlbot)
- [SQLBot Workspace Dashboard Skill Reference](reference.md)
- [SQLBot Skills README](README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown summaries with JSON command output and exported JPG, PNG, or PDF dashboard files when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save skill-local datasource state and write dashboard export files; SQLBot API credentials are required.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
