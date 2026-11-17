## Description:

Scoro API v2 integration for time tracking, task management, utilization reporting, team status reports, and billable corrections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[germainsafari](https://clawhub.ai/user/germainsafari)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, managers, and operations teams use this skill to query Scoro tasks and time entries, prepare utilization and team status reports, and correct billable status on time entries with explicit authorization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configured Scoro API key can give the agent broad access to company tasks, time entries, users, projects, contacts, and financial records.

Mitigation: Use a dedicated least-privilege Scoro API key and do not enable finance, contact, modify, or delete permissions unless the deployment explicitly requires them.

Risk: A configurable company URL could send the API key to the wrong endpoint if it is misconfigured.

Mitigation: Verify SCORO_COMPANY_URL is exactly the organization's HTTPS Scoro tenant API URL before enabling the skill.

Risk: Team reports can expose sensitive employee productivity and utilization data.

Mitigation: Require clear user authorization for team reporting and limit access to users who are allowed to view employee time data.

Risk: Billable-status corrections and other modify or delete actions can change business records.

Mitigation: Require explicit user confirmation before any modifying action and review the target record IDs before execution.

## Reference(s):

- [Scoro API v2](https://api.scoro.com/api/v2)
- [ClawHub Scoro Skill](https://clawhub.ai/germainsafari/skills/scoro)
- [ClawHub Publisher Profile](https://clawhub.ai/user/germainsafari)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON, shell, and PowerShell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide API calls that read or modify Scoro records when configured with a Scoro API key and tenant URL.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
