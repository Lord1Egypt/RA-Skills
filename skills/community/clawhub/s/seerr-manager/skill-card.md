## Description: <br>
CLI for the Seerr media request management API that can search movies and TV shows, create and manage media requests, manage users, track issues, and administer a self-hosted Seerr instance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[electather](https://clawhub.ai/user/electather) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect an agent to a self-hosted Seerr instance for media discovery, request management, issue tracking, user administration, and system status checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes powerful Seerr administration actions, including deletion, request approval, password reset, user import, and bulk updates. <br>
Mitigation: Use a least-privilege Seerr API key and require explicit user confirmation before destructive or administrative changes. <br>
Risk: MCP HTTP no-auth mode or query-string API-key mode can expose the Seerr API key if the endpoint or logs are accessible. <br>
Mitigation: Prefer stdio or bearer-token HTTP transport; only use no-auth or query-string authentication on isolated endpoints with appropriate access controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/electather/seerr-manager) <br>
- [seerr-cli repository](https://github.com/electather/seerr-cli) <br>
- [seerr-cli releases](https://github.com/electather/seerr-cli/releases/latest) <br>
- [Seerr application](https://github.com/seerr/app) <br>
- [seerr-cli container image](https://ghcr.io/electather/seerr-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require SEERR_SERVER and SEERR_API_KEY; MCP HTTP mode may also require authentication, CORS, TLS, and logging environment variables.] <br>

## Skill Version(s): <br>
v0.8.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
