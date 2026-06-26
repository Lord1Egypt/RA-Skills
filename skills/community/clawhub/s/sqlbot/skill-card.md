## Description: <br>
Manage SQLBot workspaces, datasources, ask-data flows, and dashboards, including listing and switching workspace or datasource context, asking questions against a datasource, listing dashboards, viewing dashboard details, and exporting dashboards as JPG/PNG or PDF. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuwei-fit2cloud](https://clawhub.ai/user/xuwei-fit2cloud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to work with SQLBot from an agent environment: selecting workspaces and datasources, asking data questions, inspecting dashboards, and exporting dashboard views. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses SQLBot API credentials to query workspaces, datasources, chats, and dashboards. <br>
Mitigation: Install only for trusted SQLBot instances, use a scoped API key when available, keep the .env file out of version control, and restrict its file permissions. <br>
Risk: Dashboard export writes local JPG, PNG, or PDF files and uses the configured SQLBot frontend preview route. <br>
Mitigation: Review export output paths before execution and use a trusted SQLBot base URL. <br>


## Reference(s): <br>
- [SQLBot Workspace Dashboard Skill Reference](reference.md) <br>
- [SQLBot-skills README](README.md) <br>
- [SQLBot on ClawHub](https://clawhub.ai/xuwei-fit2cloud/sqlbot) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Text, Files] <br>
**Output Format:** [Markdown guidance with shell command invocations; script responses are JSON and dashboard exports are JPG, PNG, or PDF files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided SQLBot API credentials and may write local state or dashboard export files.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
