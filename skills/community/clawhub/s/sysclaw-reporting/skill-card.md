## Description: <br>
Report system issues and submit resource requests to SysClaw via the cross-agent communication system. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MBojer](https://clawhub.ai/user/MBojer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to submit issues, resource requests, access requests, software installation requests, service actions, deployment requests, and status checks to SysClaw, then check response notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can submit access, deployment, install, restart, and configuration requests to SysClaw through direct database writes. <br>
Mitigation: Use a narrowly scoped database role and require explicit user confirmation before submitting requests that could change systems or access. <br>
Risk: The optional notification cron wrapper can persist database credentials and write notification output into workspace memory. <br>
Mitigation: Use the cron wrapper only when credentials are stored securely, file permissions are restricted, notification output is acceptable for the workspace, and there is a cleanup path. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MBojer/sysclaw-reporting) <br>
- [Changelog](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, markdown] <br>
**Output Format:** [Markdown guidance with shell command examples and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3, psycopg2-binary, and SysClaw database connection environment variables.] <br>

## Skill Version(s): <br>
4.0.0 (source: server release evidence and changelog, released 2026-03-17) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
