## Description: <br>
Query and manage Salesforce CRM data via the Salesforce CLI (`sf`). Run SOQL/SOSL queries, inspect object schemas, create/update/delete records, bulk import/export, execute Apex, deploy metadata, and make raw REST API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ArvorCo](https://clawhub.ai/user/ArvorCo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Salesforce administrators use this skill to query, inspect, and manage Salesforce org data and metadata through the authenticated Salesforce CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated Salesforce CLI access can expose or modify CRM data and org configuration. <br>
Mitigation: Use a sandbox or least-privilege Salesforce account and verify the target org before running commands. <br>
Risk: Write, delete, bulk, Apex, deployment, and raw API operations can have high-impact effects. <br>
Mitigation: Require explicit approval for those operations and review files, queries, and command targets before execution. <br>
Risk: Authentication output may contain sensitive tokens or key material. <br>
Mitigation: Do not paste or summarize tokens, SFDX auth URLs, JWT keys, or verbose auth output into chat or logs. <br>


## Reference(s): <br>
- [Salesforce CLI](https://developer.salesforce.com/tools/salesforcecli) <br>
- [ClawHub Salesforce Skill](https://clawhub.ai/ArvorCo/salesforce) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API calls, Code, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands generally request structured Salesforce CLI output with --json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
