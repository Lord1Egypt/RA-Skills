## Description:

Expose a local API service to the public internet via aitun tunnel for external testing and integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ctz168](https://clawhub.ai/user/ctz168)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to expose a local REST, GraphQL, gRPC, WebSocket, or HTTP API through a public tunnel for external testing, QA, and integration work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose local services to the public internet.

Mitigation: Expose only APIs intended for external testing, avoid secret-bearing debug endpoints or admin panels, and stop the tunnel when testing is complete.

Risk: The skill includes curl-to-bash and PowerShell installer commands.

Mitigation: Prefer pinned package-manager installation in an isolated environment and review installer contents before use.

Risk: Tunneled services may be reachable by unintended clients.

Mitigation: Use application-level authentication, rate limiting, and CORS controls appropriate for the test audience.

## Reference(s):

- [AiTun homepage](https://aitun.cc)
- [ClawHub skill page](https://clawhub.ai/ctz168/skills/remote-api)
- [ClawHub metadata link](https://clawhub.ai/ctz168/remote-api)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and endpoint examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides the agent through installing aitun, starting a local service, creating a tunnel, sharing a public URL, testing endpoints, and cleaning up.]

## Skill Version(s):

1.0.6 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
