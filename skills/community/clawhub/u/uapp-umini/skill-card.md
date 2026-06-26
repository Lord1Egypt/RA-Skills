## Description: <br>
Helps agents query read-only Umeng mini-program, H5, and mini-game analytics through umeng-cli call, covering overview, total users, retention, page, share, and custom event data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[squall0925](https://clawhub.ai/user/squall0925) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and operators use this skill to retrieve and summarize Umeng analytics for mini-program, H5, and mini-game properties. It is intended for read-only questions about application overview metrics, retention, page visits, sharing performance, and custom events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs agents to send usage and AppKey telemetry with umeng-cli trace without a clear consent step. <br>
Mitigation: Disable or decline automatic trace behavior unless telemetry is explicitly desired, and do not send AppKeys before consent. <br>
Risk: The skill depends on the Umeng CLI and local credential caching for authenticated API access. <br>
Mitigation: Install the CLI only from trusted sources, use a least-privileged Umeng account, and review local credential storage before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/squall0925/uapp-umini) <br>
- [Umeng CLI homepage](https://github.com/umeng/umeng-cli) <br>
- [Umeng OpenAPI gateway](https://gateway.open.umeng.com/openapi) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, markdown] <br>
**Output Format:** [Markdown with inline bash command examples and JSON API parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only Umeng analytics queries; requires umeng-cli installation and Umeng authentication.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
