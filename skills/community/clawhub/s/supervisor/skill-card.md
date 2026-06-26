## Description: <br>
Supervisor aggregates active tasks, open issues, monitored groups, pending follow-ups, and system health into structured status reports for a PA agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[netanel-abergel](https://clawhub.ai/user/netanel-abergel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
PA owners and admins use this skill to request quick or full status reports across active tasks, group activity, pending follow-ups, billing health, backups, and PA network status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read broad PA and WhatsApp memory, which may include private operational context. <br>
Mitigation: Limit invocation to explicit status requests, enforce requester and scope checks, and avoid full reports outside owner or admin DMs. <br>
Risk: The billing check can use an API key for a live external request. <br>
Mitigation: Require confirmation or cached results for live billing checks, protect API keys, and redact credentials and raw API responses from reports. <br>
Risk: Status workflows may lead to outbound follow-up messages or reports to other people. <br>
Mitigation: Require approval before outbound messages and log what was sent and to whom. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Structured Markdown status reports with optional shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read local PA memory files and summarize only the requester-appropriate scope.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
