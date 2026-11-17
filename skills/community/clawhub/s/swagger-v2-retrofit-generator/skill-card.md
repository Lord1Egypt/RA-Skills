## Description:

Generate Android Retrofit/Kotlin client code from Swagger v2 (OpenAPI 2.0) API documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[opoojkk](https://clawhub.ai/user/opoojkk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to fetch Swagger v2 API documentation and generate Android Retrofit service interfaces and Kotlin data classes. It supports selective generation by path, method, tag, or keyword search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Kotlin source can reflect incorrect or unsafe Swagger input.

Mitigation: Review generated Kotlin before compiling or shipping it, especially API paths, request bodies, response models, and authentication handling.

Risk: Credentials may be supplied through command-line arguments or query-string API keys.

Mitigation: Use trusted HTTPS endpoints, short-lived read-only credentials, and safer secret handling methods; avoid query-string API keys when possible.

Risk: Fetching Swagger documents from untrusted or internal-only URLs may expose network access or process untrusted API specifications.

Mitigation: Fetch only from trusted Swagger sources and avoid internal-only or untrusted URLs unless the network exposure has been reviewed.

## Reference(s):

- [Swagger v2 Structure Reference](references/swagger-v2-structure.md)
- [Retrofit + Kotlin Template Reference](references/retrofit-templates.md)

## Skill Output:

**Output Type(s):** [code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python command examples and generated Kotlin source files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated Kotlin can be written to stdout or to a user-specified output file.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
