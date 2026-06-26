## Description: <br>
Query Salesforce data and manage sales pipelines with the `sf` CLI, including SOQL queries, opportunity analysis, forecast reporting, exports, schema exploration, and CRM record operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rjmcgirr-pl](https://clawhub.ai/user/rjmcgirr-pl) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, sales operations teams, and CRM administrators use this skill to query Salesforce, review pipeline health, prepare deal and forecast summaries, and draft `sf` CLI commands for CRM data work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use an agent's Salesforce CLI session to read or export sensitive CRM data such as contacts, account notes, opportunity details, and pipeline reports. <br>
Mitigation: Verify the target org before use, prefer sandbox or least-privilege accounts, and treat exported CRM data as confidential business data. <br>
Risk: The skill includes Salesforce CLI patterns for creating, updating, importing, and bulk upserting records. <br>
Mitigation: Require explicit approval before any export, import, bulk upsert, or record-changing command, and review target objects, filters, and record IDs before execution. <br>


## Reference(s): <br>
- [Salesforce ClawHub release](https://clawhub.ai/rjmcgirr-pl/salesforce-dx) <br>
- [Pipeline & Forecast Queries](references/pipeline-queries.md) <br>
- [Advanced SOQL Patterns](references/soql-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline SOQL and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Salesforce CLI commands that read, export, create, update, import, or bulk upsert CRM records.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
