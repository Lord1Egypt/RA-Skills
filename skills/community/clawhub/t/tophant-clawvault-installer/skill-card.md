## Description:

Install, configure, test, and uninstall ClawVault AI security proxy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[martin2877](https://clawhub.ai/user/martin2877)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to install and manage ClawVault as a local AI security proxy, generate security rules, run detection tests, and remove proxy configuration when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default setup can inspect API prompts, responses, and credentials through a local HTTPS inspection proxy.

Mitigation: Review before installing on a machine with real credentials and prefer a disposable VM or container for initial evaluation.

Risk: The installer uses mutable remote code from the ClawVault main branch rather than a pinned release.

Mitigation: Install only from an audited pinned ClawVault commit for sensitive environments.

Risk: Proxy integration can make persistent OpenClaw gateway changes and gateway restart may affect active sessions.

Mitigation: Use --no-proxy and --no-start unless proxy activation is intentional, and avoid --restart-gateway until the TLS and connectivity impact is understood.

## Reference(s):

- [ClawVault repository](https://github.com/tophant-ai/ClawVault)
- [ClawVault OpenClaw skill guide](https://github.com/tophant-ai/ClawVault/blob/main/doc/OPENCLAW_SKILL.md)
- [ClawVault documentation](https://github.com/tophant-ai/ClawVault/tree/main/doc)
- [ClawHub skill page](https://clawhub.ai/martin2877/skills/tophant-clawvault-installer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with bash command examples and JSON-capable command output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands support --json for machine-readable output.]

## Skill Version(s):

0.2.13 (source: server release, SKILL.md frontmatter, skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
