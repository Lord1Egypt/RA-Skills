## Description:

WebSocket connection management with exponential backoff + jitter retry, heartbeat detection, and circuit breaker pattern.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qwe123sddfsdfs](https://clawhub.ai/user/qwe123sddfsdfs)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to add resilient WebSocket clients that reconnect after network failures, detect stale connections with heartbeats, and limit repeated failures with a circuit breaker.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence reports a suspicious verdict because the central WebSocket dependency setup includes a reported-vulnerable ws version and a third-party package mirror.

Mitigation: Review before production use, regenerate the lockfile from the official npm registry, upgrade ws to a patched reviewed version, and enforce installation with npm ci or equivalent lockfile controls.

Risk: WebSocket peers can be untrusted connection targets, and examples show configurable headers that could carry sensitive tokens.

Mitigation: Treat peers as untrusted unless controlled, validate connection targets, and avoid passing sensitive headers or tokens unless the target is trusted.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/qwe123sddfsdfs/skills/websocket-reconnect)
- [Publisher Profile](https://clawhub.ai/user/qwe123sddfsdfs)
- [ws package tarball from resolved package lock](https://registry.npmmirror.com/ws/-/ws-8.19.0.tgz)

## Skill Output:

**Output Type(s):** [code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JavaScript code examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and the ws package for Node.js usage.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
