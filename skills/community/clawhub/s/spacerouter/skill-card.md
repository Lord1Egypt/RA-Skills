## Description:

Route HTTP traffic through Space Router residential IP proxy network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taelimoh](https://clawhub.ai/user/taelimoh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use SpaceRouter to route HTTP requests through Space Router's residential proxy network when direct requests are blocked by datacenter IP filtering, CAPTCHA challenges, or similar IP-based controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Proxy credentials can be exposed through shell history, logs, screenshots, or source control.

Mitigation: Store SPACE_ROUTER_PROXY_URL only in local environment configuration or a secrets manager and avoid printing it in commands or logs.

Risk: The proxy provider may see proxy metadata and non-TLS request contents.

Mitigation: Use the proxy only for intended routing tasks, avoid sensitive destinations, and prefer HTTPS targets.

Risk: Unpinned SDK or CLI installs may change proxy behavior over time.

Mitigation: Pin or review Space Router SDK and CLI versions before installing them in persistent environments.

## Reference(s):

- [SpaceRouter ClawHub Skill Page](https://clawhub.ai/taelimoh/skills/spacerouter)
- [Space Router Gateway](https://gateway.spacerouter.org)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown with bash, Python, TypeScript, and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SPACE_ROUTER_PROXY_URL containing the Space Router proxy URL and API key credentials.]

## Skill Version(s):

0.2.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
