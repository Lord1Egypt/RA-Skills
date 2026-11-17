## Description:

Purchase and manage SOCKS5 residential proxies via ProxyBase API with cryptocurrency payments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[proxybase-user](https://clawhub.ai/user/proxybase-user)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and OpenClaw users use this skill to register with ProxyBase, create cryptocurrency-funded proxy orders, poll for activation, and configure SOCKS5 proxy access for selected agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ProxyBase credentials and proxy secrets are stored in the skill state directory.

Mitigation: Treat the state directory as sensitive, restrict local access to it, and prefer non-executable secret storage with strict file permissions before production use.

Risk: Changing PROXYBASE_API_URL can direct registration, order, and credential traffic to an unintended API origin.

Mitigation: Set PROXYBASE_API_URL only to the real ProxyBase API endpoint and validate API origin before use.

Risk: The inject-gateway flow can persistently reroute OpenClaw gateway traffic through the proxy.

Mitigation: Run inject-gateway only after explicit user confirmation, review the service changes, and keep a clear rollback path.

## Reference(s):

- [ProxyBase homepage](https://proxybase.xyz)
- [ProxyBase API base](https://api.proxybase.xyz/v1)
- [ClawHub skill page](https://clawhub.ai/proxybase-user/skills/proxybase-openclaw-skill)
- [Publisher profile](https://clawhub.ai/user/proxybase-user)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include payment instructions, polling status, proxy credentials, state file paths, and OpenClaw proxy configuration guidance.]

## Skill Version(s):

1.0.12 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
