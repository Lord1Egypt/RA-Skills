## Description:

Compiles a Python-backed agent skill into a standalone REST API microservice that executes the skill by subprocess and returns a structured response envelope.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songhonglei](https://clawhub.ai/user/songhonglei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to expose a single Python skill as a local or deployed HTTP API for tools, CI pipelines, services, and client applications that need structured skill execution without a runtime gateway.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated HTTP service can expose the wrapped skill's execution surface to any caller that can reach the endpoint.

Mitigation: Bind the service to localhost unless network access is intentional, set FLASH_API_KEY, restrict CORS, and use HTTPS for cross-host calls.

Risk: Async mode can retain sensitive or very large outputs in job history.

Mitigation: Avoid async mode for sensitive workloads unless job history storage and access are protected.

## Reference(s):

- [Migration from v1](references/migration-from-v1.md)
- [Standalone usage](references/standalone-usage.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands plus generated Python service code and JSON configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a REST response envelope with success, exit_code, elapsed_ms, data or output, stderr, and truncation metadata for wrapped skill calls.]

## Skill Version(s):

2.0.4 (source: server release metadata and artifact README/SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
