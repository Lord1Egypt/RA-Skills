## Description: <br>
Helps Taobao store operators generate daily operations reports, compliance checks, inventory reminders, customer-service logs, after-sales records, and risk alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guowaa223](https://clawhub.ai/user/guowaa223) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ecommerce operators use this skill to produce local Taobao operations reports, compliance review sheets, inventory checks, customer-service response logs, after-sales records, and risk-control alerts for human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review flagged a mismatch between read-only and manual-approval claims and the documented customer auto-reply and after-sales automation behavior. <br>
Mitigation: Review before connecting a real Taobao account; do not provide write-capable credentials or enable live customer replies, refunds, or after-sales automation until explicit approvals, API scopes, start/stop controls, and audit controls are documented and enforced. <br>
Risk: Generated operations, compliance, inventory, and after-sales outputs could influence store decisions or customer interactions. <br>
Mitigation: Treat outputs as local reports for human review and manually verify recommendations before making changes in Taobao or communicating with customers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guowaa223/taobao-operations) <br>
- [Publisher profile](https://clawhub.ai/user/guowaa223) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown instructions and CLI output; generated artifacts include Excel .xlsx reports, JSON customer-service logs, and local log files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3 with requests, pandas, and openpyxl; artifact metadata declares win32 support.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
