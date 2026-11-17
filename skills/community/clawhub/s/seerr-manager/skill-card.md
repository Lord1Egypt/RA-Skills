## Description:

CLI for the Seerr media request management API that lets agents search movies and TV shows, create and manage media requests, manage users, track issues, and administer a self-hosted Seerr instance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[electather](https://clawhub.ai/user/electather)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate a self-hosted Seerr media request server from an agent, including search, request handling, user administration, issue tracking, and system status checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform powerful Seerr administration actions, including user, request, media, issue, watchlist, and blocklist changes.

Mitigation: Use a least-privileged Seerr API key and review proposed destructive actions before execution.

Risk: HTTP MCP transport can expose Seerr access if authentication, network binding, or TLS are configured weakly.

Mitigation: Prefer stdio or bearer-token HTTP, bind HTTP to localhost or a protected network, use TLS for non-local access, and avoid no-auth mode.

Risk: Allowing API keys in URL query parameters can leak credentials through logs, browser history, or intermediaries.

Mitigation: Avoid API keys in URLs where possible and prefer headers or stdio-based operation.

Risk: Installation depends on a third-party release archive or container image supply chain.

Mitigation: Install only from trusted electather releases, verify checksums, and prefer pinned versions or container digests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/electather/skills/seerr-manager)
- [Publisher profile](https://clawhub.ai/user/electather)
- [seerr-cli repository](https://github.com/electather/seerr-cli)
- [seerr-cli releases](https://github.com/electather/seerr-cli/releases/latest)
- [Seerr application](https://github.com/seerr/app)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May rely on Seerr server URL and API key environment variables; CLI commands return JSON.]

## Skill Version(s):

v0.8.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
