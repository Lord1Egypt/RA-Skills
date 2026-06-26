## Description: <br>
日用品保质期管理 helps an agent create and maintain a Feishu Bitable for household item shelf-life records, queries, deletion, used-up marking, and daily expiration reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haoxingyao](https://clawhub.ai/user/haoxingyao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external users can use this skill through an agent to track household or workplace consumables, record expiration dates, find items that are close to expiring, and receive daily Feishu reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create and manage Feishu Bitable resources and transfer ownership to the current Feishu user. <br>
Mitigation: Review the initialization behavior before installing and confirm that the target Feishu user should own the created Bitable. <br>
Risk: The skill stores Bitable and cron identifiers in a local configuration file. <br>
Mitigation: Restrict access to the local skill workspace and inspect the configuration file after setup. <br>
Risk: The skill starts a recurring daily reminder job that may send expiration data through Feishu. <br>
Mitigation: Confirm reminder setup during installation and disable or remove the cron job when reminders are no longer wanted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/haoxingyao/shelflife) <br>
- [Publisher profile](https://clawhub.ai/user/haoxingyao) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, API calls, text] <br>
**Output Format:** [Natural-language responses with Feishu Bitable operations and local configuration updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create Feishu Bitable resources, store table and cron identifiers locally, and schedule daily reminder checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
