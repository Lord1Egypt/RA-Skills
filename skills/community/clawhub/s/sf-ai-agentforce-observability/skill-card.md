## Description: <br>
Agentforce session tracing extraction and analysis for Salesforce Data Cloud telemetry, STDM records, Parquet datasets, and trace-driven debugging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dsouza-anush](https://clawhub.ai/user/dsouza-anush) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Salesforce administrators, platform engineers, and agent developers use this skill to extract Agentforce Session Tracing Data Model telemetry, analyze Parquet datasets, reconstruct session timelines, and diagnose topic routing, action failures, latency, or quality issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access and export sensitive Agentforce and Data 360 telemetry, including prompts, messages, action inputs and outputs, logs, and quality traces. <br>
Mitigation: Install and run it only for authorized Salesforce administrators or engineers, use narrow date and session filters, store exports in protected locations, redact data before sharing, and delete exports when no longer needed. <br>
Risk: Broad extraction or analysis over large telemetry windows can increase data exposure and query cost. <br>
Mitigation: Prefer focused extraction by date range, agent, or session ID, and avoid unnecessary full-history pulls. <br>
Risk: The internal Builder trace and HAR capture workflow may expose highly sensitive trace and browser data. <br>
Mitigation: Avoid that workflow unless the organization has explicitly approved it and has defined handling rules for the captured files. <br>


## Reference(s): <br>
- [Data Model Reference](references/data-model-reference.md) <br>
- [Authentication Setup](references/auth-setup.md) <br>
- [CLI Reference](references/cli-reference.md) <br>
- [Analysis Cookbook](references/analysis-cookbook.md) <br>
- [Salesforce Data Cloud Query API](https://developer.salesforce.com/docs/atlas.en-us.c360a_api.meta/c360a_api/c360a_api_query.htm) <br>
- [Salesforce Agentforce Session Tracing](https://help.salesforce.com/s/articleView?id=sf.copilot_session_tracing.htm) <br>
- [Salesforce JWT Bearer Flow](https://help.salesforce.com/s/articleView?id=sf.remoteaccess_oauth_jwt_flow.htm) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python snippets, configuration steps, and analysis summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Parquet extraction artifacts and analysis reports when the bundled scripts are run by an authorized user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
