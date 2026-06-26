## Description: <br>
Give an OpenClaw agent scoped API access for Docker container management, marketplace app installs, and multi-machine WAGMIOS host administration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mentholmike](https://clawhub.ai/user/mentholmike) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and homelab administrators use this skill to let an agent manage Docker containers and WAGMIOS marketplace apps through scoped API keys across one or more hosts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can administer Docker and WAGMIOS hosts, including creating, stopping, deleting, and installing containers or apps. <br>
Mitigation: Use separate least-privilege API keys per host and require explicit user confirmation before installs, stops, deletes, image pulls or deletes, and multi-host changes. <br>
Risk: Container logs and configuration output can contain sensitive service, path, or credential-adjacent information. <br>
Mitigation: Treat logs and configuration output as sensitive and avoid exposing full API keys or unnecessary host details. <br>
Risk: A missing or excessive scope can either block intended tasks or grant broader host control than needed. <br>
Mitigation: Check GET /api/auth/status before actions and ask the user to adjust scopes in WAGMIOS settings rather than attempting workarounds. <br>


## Reference(s): <br>
- [WAGMIOS ClawHub Release](https://clawhub.ai/mentholmike/wagmios) <br>
- [API Reference](references/api.md) <br>
- [Docker Installation Guide](references/docker-install.md) <br>
- [Marketplace Reference](references/marketplace.md) <br>
- [Safeguards](references/safeguards.md) <br>
- [Scope Reference](references/scopes.md) <br>
- [Workflows](references/workflows.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline API requests, JSON examples, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided WAGMIOS base URL and scoped X-API-Key at runtime.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
