## Description: <br>
Complete Salesforce CRM integration for real-time data access, lead management, opportunity tracking, duplicate detection, and bulk operations with OAuth connection support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sawera557](https://clawhub.ai/user/sawera557) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales and revenue teams use this skill to connect an agent to Salesforce, query CRM records, manage leads, opportunities, accounts, and contacts, detect duplicates, and perform controlled bulk operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform live Salesforce read, write, bulk, and automation operations. <br>
Mitigation: Use a dedicated least-privilege Salesforce integration user and require human confirmation before destructive or bulk changes. <br>
Risk: Automation features may require high-impact metadata-level authority. <br>
Mitigation: Test standardization and Flow deployment behavior in a Salesforce sandbox before using it in production. <br>
Risk: Some documented safeguards may be incomplete or overstated, and command output may expose customer data. <br>
Mitigation: Do not rely on documented encryption, timeout, validation-rule, or rollback claims without independent controls; protect logs and shared transcripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sawera557/salesforce-easy) <br>
- [Salesforce guide](salesforce-guide.html) <br>
- [Skill documentation](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown or plain text responses with tables, Salesforce record identifiers, status summaries, and shell command snippets when setup is needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Salesforce customer data or record IDs in agent output; protect transcripts, logs, and command output.] <br>

## Skill Version(s): <br>
1.0.17 (source: server release metadata; artifact SKILL.md frontmatter reports 1.0.0 and _meta.json reports 1.0.16) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
