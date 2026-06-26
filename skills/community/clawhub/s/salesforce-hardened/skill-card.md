## Description: <br>
Query and manage Salesforce CRM data via the Salesforce CLI (`sf`). Run SOQL/SOSL queries, inspect object schemas, create/update/delete records, bulk import/export, execute Apex, deploy metadata, and make raw REST API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, administrators, and support teams use this skill to generate and review Salesforce CLI commands for querying CRM data, inspecting metadata, managing records, deploying metadata, executing Apex, and making authenticated API requests. It is intended for authenticated Salesforce environments where users can review commands before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Salesforce access tokens, refresh-token-bearing SFDX auth URLs, JWT key contents, and full org-display JSON can be exposed during normal CLI workflows. <br>
Mitigation: Use a secure secret-handling and redaction process, and do not print or share those values in agent responses. <br>
Risk: Create, update, delete, deployment, Apex, bulk, and raw REST operations can modify production data or metadata. <br>
Mitigation: Require explicit user approval before those operations, and confirm the target org before destructive operations when multiple orgs are connected. <br>
Risk: CRM data, customer PII, financial records, and org metadata can be exfiltrated if query or API output is piped to network-transmitting commands. <br>
Mitigation: Do not pipe Salesforce outputs to network commands; export locally and use an approved secure transfer process outside the agent workflow. <br>
Risk: Soft-deleted or archived records may be sensitive because they can include data removed for compliance or privacy reasons. <br>
Mitigation: Use `--all-rows` only when the user explicitly requests deleted, soft-deleted, or archived records; otherwise query active records first. <br>


## Reference(s): <br>
- [Salesforce CLI](https://developer.salesforce.com/tools/salesforcecli) <br>
- [Faberlens Salesforce Safety Evaluation](https://faberlens.ai/explore/salesforce) <br>
- [ClawHub Salesforce Hardened Skill](https://clawhub.ai/snazar-faberlens/salesforce-hardened) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash, SOQL, SQL, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands assume the Salesforce CLI is installed and the target org is authenticated; structured command output should use `--json` where supported.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
