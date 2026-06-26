## Description: <br>
Analyze Sentry error patterns, prioritize issues by user impact, identify root causes, and suggest targeted fixes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to triage Sentry issues, group related failures by root cause, rank them by user impact, and produce focused repair plans for crashes, regressions, and error spikes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes example Sentry API commands that require an authentication token. <br>
Mitigation: Review commands before execution and use a narrowly scoped read-only Sentry token when possible. <br>
Risk: Sentry logs, stack traces, and event payloads may contain secrets or unnecessary personal data. <br>
Mitigation: Redact secrets and unnecessary personal data before sharing inputs with an agent or including them in reports. <br>


## Reference(s): <br>
- [Sentry Issues API](https://sentry.io/api/0/projects/{org}/{project}/issues/?query=is:unresolved&sort=freq&limit=50) <br>
- [Sentry Issue Events API](https://sentry.io/api/0/issues/{issue_id}/events/?limit=10) <br>
- [Sentry Issue Tags API](https://sentry.io/api/0/issues/{issue_id}/tags/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown report with structured sections and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces prioritized issue rankings, root cause analysis, mitigation guidance, and sprint planning recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
