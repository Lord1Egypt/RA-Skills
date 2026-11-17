## Description:

Build REST API specifications for Sling data extraction, including authentication, pagination, response processing, rate limiting, endpoint chaining, and incremental sync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flarco](https://clawhub.ai/user/flarco)

### License/Terms of Use:


## Use Case:

Developers and data engineers use this skill to author and review Sling REST API extraction specifications. It is intended for configuring GET-based extraction workflows with authentication, pagination, response parsing, queues, dynamic endpoints, and incremental sync state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated API specs may include network-capable configuration, credentials, or response-derived download URLs.

Mitigation: Use least-privilege credentials, prefer read-only scopes, verify base URLs and response-derived URLs, and confirm OAuth token and sync-state storage before production use.

Risk: Incorrect extraction specs can produce incomplete, excessive, or unintended API requests.

Mitigation: Review generated specs, keep rate limits and concurrency conservative, and test endpoints with small limits before wider runs.

## Reference(s):

- [Sling API Specs Documentation](https://docs.slingdata.io/concepts/api-specs.md)
- [ClawHub Skill Page](https://clawhub.ai/flarco/skills/sling-api-specs)
- [AUTHENTICATION.md](AUTHENTICATION.md)
- [ENDPOINTS.md](ENDPOINTS.md)
- [REQUEST.md](REQUEST.md)
- [PAGINATION.md](PAGINATION.md)
- [RESPONSE.md](RESPONSE.md)
- [PROCESSORS.md](PROCESSORS.md)
- [VARIABLES.md](VARIABLES.md)
- [QUEUES.md](QUEUES.md)
- [INCREMENTAL.md](INCREMENTAL.md)
- [DYNAMIC.md](DYNAMIC.md)
- [FUNCTIONS.md](FUNCTIONS.md)
- [RULES.md](RULES.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with YAML and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance for authoring network-capable Sling API extraction specs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
