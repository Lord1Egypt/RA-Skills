## Description:

CLI for the Seer media request management API that helps agents search movies and TV shows, create and manage media requests, manage users, track issues, and administer a self-hosted Seer instance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[electather](https://clawhub.ai/user/electather)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and administrators use this skill to connect agents or shell workflows to a self-hosted Seer instance for media discovery, request management, user administration, issue tracking, and system status checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Powerful Seer API credentials can expose media, user, and administrative operations more broadly than expected.

Mitigation: Use a least-privileged Seer API key, store it securely, and restrict who can access the configured skill or MCP server.

Risk: Network-accessible MCP HTTP transport can be exposed without strong authentication if no-auth mode is used or route tokens are weak.

Mitigation: Prefer bearer-token authentication, bind HTTP services to localhost or a protected network, and avoid no-auth mode for network-accessible MCP servers.

Risk: Administrative actions such as delete, password reset, bulk user updates, or external media-file actions can be destructive.

Mitigation: Require explicit human confirmation before executing high-impact administrative or file-management actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/electather/skills/seer-manager)
- [seer-cli repository](https://github.com/electather/seer-cli)
- [seer-cli releases](https://github.com/electather/seer-cli/releases/latest)
- [Seer application](https://github.com/seerr/app)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command output is JSON; verbose mode may add request URLs and HTTP status before JSON.]

## Skill Version(s):

v0.4.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
