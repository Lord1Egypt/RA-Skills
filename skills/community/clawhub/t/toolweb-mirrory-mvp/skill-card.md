## Description:

Token generation and validation service for WordPress proxy and desktop application session management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

WordPress administrators, desktop application developers, and enterprises use this skill to understand Mirrory API token generation, machine-bound token validation, and service health checks for session management workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles JWT tokens, proxy secrets, WordPress user IDs, and machine IDs that could expose account or session access if logged or transmitted insecurely.

Mitigation: Send these values only over trusted HTTPS connections, avoid logging them, and confirm provider retention and revocation practices before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/toolweb-mirrory-mvp)
- [Mirrory API docs](https://api.toolweb.in:8202/docs)
- [Mirrory Kong route](https://api.toolweb.in/tools/mirrory)
- [ToolWeb](https://toolweb.in)
- [OpenAPI specification](artifact/openapi.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and OpenAPI JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes endpoint paths, request schemas, response examples, pricing information, and service links; does not execute API calls.]

## Skill Version(s):

1.0.0 (source: server release metadata and OpenAPI info.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
