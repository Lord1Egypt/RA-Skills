## Description: <br>
CLI for the Seer media request management API, including search, media requests, user management, issue tracking, system status checks, and administration for a self-hosted Seer instance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[electather](https://clawhub.ai/user/electather) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and administrators use this skill to connect an agent to a self-hosted Seer server, search media catalogs, create and manage media requests, inspect issues, and perform user or system administration tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes high-impact administration operations, including delete actions, bulk user updates, imports, password resets, and other account-changing workflows. <br>
Mitigation: Use least-privileged Seer API credentials, avoid user-administration rights unless required, and require explicit human confirmation before delete, bulk update, import, password reset, or other account-changing operations. <br>
Risk: The skill requires Seer server credentials and may run an MCP HTTP server for remote clients. <br>
Mitigation: Protect SEER_API_KEY and MCP authentication tokens, prefer authenticated transports, and avoid exposing the MCP endpoint without a secret path, bearer token, or equivalent access control. <br>


## Reference(s): <br>
- [Seer CLI repository](https://github.com/electather/seer-cli) <br>
- [Seer application repository](https://github.com/seerr/app) <br>
- [Seer CLI releases](https://github.com/electather/seer-cli/releases/latest) <br>
- [ClawHub listing](https://clawhub.ai/electather/seer-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands return JSON; verbose mode can include request URLs and HTTP status before the JSON output.] <br>

## Skill Version(s): <br>
v0.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
