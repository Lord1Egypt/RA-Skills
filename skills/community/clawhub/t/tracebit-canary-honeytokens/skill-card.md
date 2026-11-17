## Description:

Tracebit Canaries helps agents set up Tracebit decoy credentials, monitor alert emails, and guide human-supervised incident response for credential theft, prompt injection, or data exfiltration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alessandro-brucato-tracebit](https://clawhub.ai/user/alessandro-brucato-tracebit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security teams use this skill to deploy Tracebit canary tokens in agent workspaces, configure heartbeat alert checks, and investigate triggered canaries with human approval. It is intended for workspace hardening and incident-response workflows where decoy credentials can reveal unauthorized access or misuse.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs mutable remote Tracebit software, including a background daemon.

Mitigation: Review the installer source before use, prefer a pinned release, and require checksum verification for downloaded binaries.

Risk: The skill deploys decoy credentials and may expose sensitive canary cache or setup values if handled carelessly.

Mitigation: Require human confirmation before deployment, avoid printing raw canary cache contents, and avoid the fixed /tmp password file pattern called out in the security guidance.

Risk: The skill uses email, messaging, and memory-file access during alert handling.

Mitigation: Limit email access to read-only alert searches, send notifications only to the user's own channel, and require human confirmation before reading memory files.

## Reference(s):

- [Tracebit Community](https://community.tracebit.com)
- [Tracebit Community CLI](https://github.com/tracebit-com/tracebit-community-cli)
- [Tracebit CLI Releases](https://github.com/tracebit-com/tracebit-community-cli/releases/latest)
- [ClawHub Tracebit Canaries Skill](https://clawhub.ai/alessandro-brucato-tracebit/skills/tracebit-canary-honeytokens)
- [API-Based Deployment](references/api-reference.md)
- [Attack Patterns - How Canaries Detect Real Threats](references/attack-patterns.md)
- [Canary Types - Reference Guide](references/canary-types.md)
- [Incident Response Playbook - Tracebit Canary Alert](references/incident-response-playbook.md)
- [Security Compliance - Tracebit Canaries Skill](references/security-compliance.md)
- [Troubleshooting - Tracebit Canaries](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, JSON snippets, and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup checklists, canary deployment guidance, alert parsing instructions, and incident-response reports.]

## Skill Version(s):

1.0.21 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
