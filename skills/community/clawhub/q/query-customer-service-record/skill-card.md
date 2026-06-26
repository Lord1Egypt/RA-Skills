## Description: <br>
Queries and summarizes customer service records for the Huo Xiaoding customer-service system by resolving customer names, optional date ranges, and matching service-record data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adtomato](https://clawhub.ai/user/adtomato) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Customer-service and sales operations users can ask an agent to find a customer, retrieve service records for a selected date range, and produce a concise service summary. The skill is intended for authorized users of the Huo Xiaoding customer-service system. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive customer and staff service activity data. <br>
Mitigation: Install it only for users authorized to access the customer-service system, and treat returned records and summaries as confidential. <br>
Risk: The script accepts a base URL argument, which can send queries to an untrusted API destination if configured carelessly. <br>
Mitigation: Configure a trusted HTTPS API host and avoid passing arbitrary base URLs during normal use. <br>
Risk: The artifact says the current interface does not require authentication, which may provide limited built-in access control. <br>
Mitigation: Review deployment controls before use and rely on trusted network, host, or system-level authorization appropriate for the records being queried. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/adtomato/query-customer-service-record) <br>
- [Default Huo Xiaoding API host](https://hxd.ahdingtalk.com:8843) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON command output from the query script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include customer names, staff names, service counts, service types, time spans, and confidential service-record details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
