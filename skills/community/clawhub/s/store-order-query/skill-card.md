## Description: <br>
Query store order information from a MySQL database and generate order analysis reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bondli](https://clawhub.ai/user/bondli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and store operators use this skill to query MySQL store order data by date range and generate summaries of order counts, revenue, payment methods, product sales, and SKU performance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Database credentials are required and stored in the local skill configuration file. <br>
Mitigation: Use a dedicated read-only MySQL user, avoid root/admin credentials, and keep the local skill-data directory private. <br>
Risk: Generated order exports and reports can contain sensitive store order data. <br>
Mitigation: Restrict access to local orders_data.json and order_report.md files and delete old generated files when no longer needed. <br>
Risk: The skill depends on the mysql2 package for database access. <br>
Mitigation: Lock and audit the installed mysql2 version before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bondli/store-order-query) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown report, JSON order export, and setup/execution guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local orders_data.json and order_report.md files under the skill data directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
