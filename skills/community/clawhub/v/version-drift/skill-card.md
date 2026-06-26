## Description: <br>
One command to check if your entire stack is up to date. SSHes into servers, queries APIs, and compares installed versions against latest across every service you run. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rtaylorgraham](https://clawhub.ai/user/rtaylorgraham) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and infrastructure operators use Version Drift to compare installed software, service, and container versions across local machines, remote SSH hosts, and HTTP APIs against current upstream releases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured local or SSH commands can execute with the privileges of the user running the skill. <br>
Mitigation: Review config.yaml like code, use the narrowest practical account permissions, and avoid direct root SSH where possible. <br>
Risk: HTTP and SSH checks may expose sensitive infrastructure endpoints or credentials if untrusted configs are used. <br>
Mitigation: Use only configs you control, keep secrets in environment variables, and use dedicated low-privilege SSH and API credentials. <br>
Risk: Relaxing SSH host key checks or TLS verification can weaken transport security. <br>
Mitigation: Keep SSH host checking and TLS verification enabled unless there is a specific internal reason to change them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rtaylorgraham/version-drift) <br>
- [Publisher profile](https://clawhub.ai/user/rtaylorgraham) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [CLI reports as table, JSON, or Markdown; generated Docker Compose discovery output as YAML or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exit codes indicate drift or errors; optional state tracking records how long checks have been drifting.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
