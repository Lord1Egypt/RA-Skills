## Description: <br>
Manage SQLBot workspaces, datasources, ask-data flows, and dashboards, including listing and switching workspace or datasource context, asking questions against a datasource, listing dashboards, viewing dashboard details, and exporting dashboards as PNG or PDF. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuwei-fit2cloud](https://clawhub.ai/user/xuwei-fit2cloud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and SQLBot operators use this skill to manage SQLBot workspace and datasource context, ask data questions, inspect dashboards, and export dashboard views. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a SQLBot API key to access the configured SQLBot instance. <br>
Mitigation: Use a least-privilege key, keep credentials out of shared skill directories, and verify SQLBOT_BASE_URL before running commands. <br>
Risk: Workspace and datasource switches affect the context used by later SQLBot operations. <br>
Mitigation: Review requested workspace and datasource changes before execution, especially before asking data questions or viewing dashboards. <br>
Risk: Dashboard exports write PNG or PDF files to the requested output path. <br>
Mitigation: Choose export paths that will not overwrite important files. <br>


## Reference(s): <br>
- [SQLBot Workspace Dashboard Skill Reference](reference.md) <br>
- [SQLBot-skills README](README.md) <br>
- [ClawHub release page](https://clawhub.ai/xuwei-fit2cloud/sqlboot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration guidance, Files] <br>
**Output Format:** [Markdown guidance with bash commands and JSON command output; PNG or PDF files for dashboard exports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided SQLBot connection settings and API key credentials before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
