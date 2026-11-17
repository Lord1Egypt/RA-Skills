## Description:

Orchestrates a staged workflow for creating Spring Boot and Vue full-stack projects from initial requirements through UI design, frontend and backend development, integration testing, and optional Chinese thesis writing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tanboku](https://clawhub.ai/user/tanboku)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and students use this skill to coordinate the end-to-end creation of a Spring Boot 3.x, Vue 3, Vite, Element Plus, and MySQL full-stack project. It guides requirement gathering, UI prompts, implementation, testing, optional Redis/payment/AI modules, and optional thesis drafting with user confirmation between phases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow requests privileged database passwords, API keys, private keys, or payment secrets and may place them in plaintext project configuration.

Mitigation: Use least-privilege development credentials, environment-variable placeholders, or a secret manager; do not paste production secrets into the workflow.

Risk: The generated project may include local commands, dependencies, and optional integrations that run code or connect to external services.

Mitigation: Review generated commands and configuration before execution, and run the project in a controlled development environment first.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tanboku/skills/springboot-vue-builder)
- [Server-resolved GitHub provenance](https://github.com/Tanboku/springboot-vue-builder)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code blocks, shell commands, file plans, and generated project artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Phased workflow output with user confirmation checkpoints and optional component-specific configuration guidance.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
