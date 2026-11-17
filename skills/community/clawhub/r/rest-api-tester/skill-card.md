## Description:

Test REST APIs with customizable headers, authentication, request bodies, response validation, webhook checks, performance checks, and health-check automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leonardodpanda](https://clawhub.ai/user/leonardodpanda)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to debug REST endpoints, test authentication flows, validate responses and webhooks, measure response times, and automate API health checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The webhook listener example can expose captured payloads without authentication.

Mitigation: Use only synthetic webhook data unless authentication, signature validation, redaction, and access controls are added.

Risk: API tests can send credentials or sensitive request data to untrusted endpoints.

Mitigation: Use trusted endpoints and test credentials, and avoid hardcoding real secrets in examples or logs.

Risk: Full request or webhook payload logging can disclose sensitive data.

Mitigation: Redact sensitive fields and avoid logging full payloads during testing.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces reusable request, authentication, webhook listener, performance testing, and response validation snippets.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
