## Description: <br>
Helps agents support WininSales CRM sales operations, including customer search, duplicate checks, ownership lookup, customer creation, follow-up records, assignment, sharing, public-pool recovery, leads, opportunities, contracts, payments, expiry reminders, inactive-customer lists, product lookup, employee lookup, performance analysis, and daily reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hijasongithub](https://clawhub.ai/user/hijasongithub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales representatives, sales managers, and CRM operations staff use this skill to query and update WininSales CRM records, manage customers and leads, review contracts and payments, analyze performance, and draft daily reports. It is intended for CRM workflows performed under the user's own CRM authorization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and update CRM records using the user's CRM authorization. <br>
Mitigation: Install only when the agent should operate WininSales CRM with the current account's permissions, and confirm every write action before submission. <br>
Risk: CRM workflows may involve sensitive customer data, record IDs, employee assignments, or credentials. <br>
Mitigation: Review customer names, employee targets, and record IDs carefully, and avoid storing long-lived tokens or sensitive customer data in reusable files. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with structured summaries, confirmation prompts, and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include CRM record summaries, risk notices, next-step recommendations, and write-action confirmation requests.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
