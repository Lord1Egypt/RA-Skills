## Description:

Senior Python Developer guides an agent to produce production-ready, statically typed, secure Python code for containerized architectures, microservices, CLI tools, and system programming.

This skill is ready for commercial/non-commercial use.

## Publisher:

[an0nx](https://clawhub.ai/user/an0nx)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to make an agent produce production-oriented Python implementations for microservices, CLI tools, containerized services, and system programming. It emphasizes strict typing, src layout, Ruff, pytest, pydantic-settings, Docker, and security-focused coding conventions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill claims override authority and may broaden edits beyond the user's intended request.

Mitigation: Review proposed changes before applying them and use explicit scope controls such as asking for minimal changes when broad file cleanup is not desired.

Risk: The skill requires chain-of-thought style reasoning output, which is unsafe for normal agent operation.

Mitigation: Prefer a version that summarizes reasoning without requesting private chain-of-thought disclosure.

Risk: The skill mandates opinionated Python, formatting, documentation, and container defaults that may not fit an existing project.

Mitigation: Install only when those conventions match the project, and review generated dependencies, Docker images, and formatting changes before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/an0nx/skills/senior-python-developer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill directs the agent to provide complete file contents for created or modified files and to use Russian for reasoning-oriented response sections.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
