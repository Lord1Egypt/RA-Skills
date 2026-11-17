## Description:

Choose RunAPI SDK packages for application developers building web apps, backends, workers, or libraries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to choose the appropriate RunAPI SDK or provider client package for application, backend, worker, library, or production integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A developer may install the wrong or stale RunAPI package for a target model or language.

Mitigation: Verify package names and client methods against RunAPI's current documentation before adding dependencies.

Risk: A RunAPI API key may be exposed if copied into source code or committed configuration.

Mitigation: Keep RUNAPI_API_KEY in environment variables or a secret manager and do not commit secrets.

Risk: RunAPI-generated file URLs may expire before downstream systems retain the generated asset.

Mitigation: Download generated files and store them in durable application-owned storage within 7 days.

Risk: Using the RunAPI CLI as a production runtime layer can create a brittle application integration.

Mitigation: Use the relevant RunAPI SDK or provider client package for application, backend, worker, library, and production code paths.

## Reference(s):

- [RunAPI models and SDK packages](https://runapi.ai/models.md)
- [RunAPI models homepage](https://runapi.ai/models)
- [ClawHub publisher profile: runapi-ai](https://clawhub.ai/user/runapi-ai)
- [ClawHub skill page: runapi-sdk](https://clawhub.ai/runapi-ai/skills/runapi-sdk)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with package names, install commands, configuration notes, and code-oriented integration advice]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference language-specific RunAPI provider clients, RUNAPI_API_KEY handling, and durable storage guidance for generated file URLs.]

## Skill Version(s):

0.2.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
