## Description:

Generate accurate Volcengine SDK examples by locating an API through API Explorer search, fetching its swagger, and calling api/common/explorer/make-code with user-provided Params.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volc-sdk-team](https://clawhub.ai/user/volc-sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate Volcengine API SDK call examples and related SDK configuration guidance for Python, Go, Java, PHP, cURL, and Node.js.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes copy-ready SDK configuration examples that disable TLS or certificate verification.

Mitigation: Keep HTTPS and certificate verification enabled, and use disable-SSL or verify-false settings only in tightly controlled test scenarios.

Risk: User-supplied API Params are sent to Volcengine API Explorer during code generation.

Mitigation: Do not include secrets or sensitive production data in Params passed to the skill.

## Reference(s):

- [Volcengine SDK Generator Skill](https://clawhub.ai/volc-sdk-team/skills/volcengine-sdk-generator)
- [Volcengine API Explorer common API](https://api.volcengine.com/api/common)
- [Go SDK Integration Reference](references/sdk-integration-go.md)
- [Python SDK Integration Reference](references/sdk-integration-python.md)
- [Java SDK Integration Reference](references/sdk-integration-java.md)
- [Node.js SDK Integration Reference](references/sdk-integration-nodejs.md)
- [PHP SDK Integration Reference](references/sdk-integration-php.md)

## Skill Output:

**Output Type(s):** [Code, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with SDK code blocks and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include mocked required top-level API parameters when the user omits them; user-supplied Params are sent to Volcengine API Explorer.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
