## Description:

Analyze Spring Boot Actuator endpoints for security, health checks, metrics exposure, and production configuration, including info, health, and custom endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to audit Spring Boot Actuator configuration, endpoint exposure, health checks, metrics, and production readiness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides inspection of Spring Boot configuration and source files, which may expose sensitive application details to the reviewing agent.

Mitigation: Run it only in projects where the agent is authorized to read configuration and source files.

Risk: Suggested Actuator configuration changes may be incomplete or unsuitable for a specific production environment.

Mitigation: Review all recommendations manually before applying them.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory, read-only analysis based on project configuration and source files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
