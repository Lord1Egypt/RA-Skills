## Description: <br>
Executes SQL queries, organizes results with a Jinja2 template, and writes the generated report to a Feishu cloud document. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runkecheng](https://clawhub.ai/user/runkecheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and data operators use this skill to turn DataWorks or MaxCompute SQL results into templated Feishu documents for recurring reports, data summaries, and one-off analysis outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run broad SQL queries against DataWorks or MaxCompute data. <br>
Mitigation: Install only for users authorized to query the relevant data, use read-only least-privileged credentials, and confirm the exact SQL before each run. <br>
Risk: The skill can publish query results into Feishu documents where destination visibility may expose sensitive data. <br>
Mitigation: Confirm the destination, document visibility, and notification recipient before each run, and avoid exporting sensitive data unless the workflow is organization-approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/runkecheng/sql-to-doc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API Calls, guidance] <br>
**Output Format:** [Feishu cloud document link and document creation status, with templated Markdown-style report content.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires META_CENTER_TOKEN and DATAWORKS_PROJECT environment variables; may optionally notify a Feishu user after document creation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
