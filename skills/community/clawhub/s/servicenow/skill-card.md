## Description: <br>
Connects an AI agent to ServiceNow so it can query, create, update, delete, aggregate, inspect schema, manage attachments, and check instance health through ServiceNow REST APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onlyflowstech](https://clawhub.ai/user/onlyflowstech) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, ITSM teams, ITOM teams, and ServiceNow operators use this skill to let an agent work with incidents, changes, problems, CMDB records, knowledge articles, attachments, bulk record operations, and instance health checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, delete, and bulk-modify ServiceNow records when configured with an account that has those permissions. <br>
Mitigation: Use a dedicated least-privilege ServiceNow API user and review write, delete, and batch commands before execution. <br>
Risk: Bulk operations can affect many records if the encoded query is too broad. <br>
Mitigation: Keep batch operations in dry-run mode until the matched records and limits are verified, then require explicit confirmation to execute. <br>
Risk: Attachment upload and download operations can move data between the local machine and ServiceNow. <br>
Mitigation: Review attachment paths, record targets, and data handling requirements before running attachment commands. <br>


## Reference(s): <br>
- [ClawHub ServiceNow skill page](https://clawhub.ai/onlyflowstech/servicenow) <br>
- [OnlyFlows publisher profile](https://clawhub.ai/user/onlyflowstech) <br>
- [OnlyFlows homepage](https://onlyflows.tech) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq plus SN_INSTANCE, SN_USER, and SN_PASSWORD environment variables.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
