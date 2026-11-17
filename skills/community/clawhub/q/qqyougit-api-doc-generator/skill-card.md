## Description:

Generates Chinese API documentation from code, URLs, OpenAPI files, or interface descriptions, including OpenAPI 3.0/Swagger specs, SDK examples, mock server configuration, and integration tests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qqyougitcom](https://clawhub.ai/user/qqyougitcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and API teams use this skill to turn backend code, existing OpenAPI definitions, URLs, or natural-language endpoint descriptions into publishable API reference material and supporting examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated cURL, SDK, DELETE, npm, or pip commands may cause unwanted network calls, resource changes, or package installs if run blindly.

Mitigation: Review URLs, tokens, package publishers, target resource IDs, and command intent before execution; prefer test environments for generated examples.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qqyougitcom/skills/qqyougit-api-doc-generator)
- [Detailed API documentation generator reference](artifact/references/details.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with OpenAPI YAML, SDK code examples, cURL commands, mock server configuration, and test snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Primary language is Chinese documentation with English comments in code examples.]

## Skill Version(s):

2.0.0 (source: ClawHub release evidence; artifact frontmatter says 1.5.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
