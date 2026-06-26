## Description: <br>
This skill integrates with Scoro API v2 for time tracking, task management, utilization reporting, team status reports, and billable corrections. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[germainsafari](https://clawhub.ai/user/germainsafari) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and business operations users use this skill to query Scoro tasks, time entries, hours, utilization, and team status, and to prepare billable-status corrections with explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Scoro API key may grant broad access to sensitive company records. <br>
Mitigation: Use a least-privileged Scoro key and require the agent to show exact records before using company data. <br>
Risk: Modify and delete endpoints could change or remove business records beyond the main time-tracking workflow. <br>
Mitigation: Require explicit user confirmation and a preview of planned changes before any modify or delete request. <br>


## Reference(s): <br>
- [Scoro API v2](https://api.scoro.com/api/v2) <br>
- [ClawHub Scoro release page](https://clawhub.ai/germainsafari/scoro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SCORO_API_KEY and SCORO_COMPANY_URL; modifying or deleting records requires explicit user permission.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
