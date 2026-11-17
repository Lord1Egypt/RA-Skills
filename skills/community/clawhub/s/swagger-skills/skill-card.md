## Description:

Use this skill to turn Swagger UI or OpenAPI/Swagger documentation links into organized API calling skills, including Python clients, field references, domain configuration, and feature navigation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jajay-liang](https://clawhub.ai/user/jajay-liang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to convert Swagger UI or OpenAPI/Swagger documentation into maintainable API-calling skills with generated Python clients, field references, domain configuration, and feature indexes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documentation credentials can be exposed through sources.json or generated configuration.

Mitigation: Use placeholders or disposable credentials during generation, avoid committing real documentation passwords, and remove doc_auth from generated outputs before sharing.

Risk: The generator may install Python packages automatically into the active environment.

Mitigation: Run it in a disposable virtual environment and review requirements before execution.

Risk: Generated API clients can send requests to domains derived from supplied Swagger/OpenAPI sources.

Mitigation: Use only trusted documentation sources and verify generated API domains before allowing callers to send data.

## Reference(s):

- [References README](artifact/references/README.md)
- [API Clients README](artifact/api_clients/README.md)
- [ClawHub Skill Page](https://clawhub.ai/jajay-liang/skills/swagger-skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, generated Python files, JSON configuration, and OpenAPI reference markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated skills may include controller-grouped API clients, OpenAPI field references, domain configuration, and an OpenAPI field index.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
