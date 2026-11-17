## Description:

Build full-stack applications after collecting project requirements, including React, Vite, Tailwind, Express, and MongoDB starter scaffolds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chinmayagit](https://clawhub.ai/user/chinmayagit)

### License/Terms of Use:


## Use Case:

Developers use this skill to collect application requirements and scaffold a full-stack web application starter with a React frontend, Node/Express backend, MongoDB configuration, JWT authentication, and an MVC project structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scaffolding script can overwrite writable paths if pointed at an existing or unintended target.

Mitigation: Use a safe new project name under the intended directory and avoid existing targets until path validation and overwrite protection are added.

Risk: The generated authenticated API is reported to have serious authorization gaps.

Mitigation: Treat the backend as a prototype until object-level authorization and update field whitelisting are fixed.

Risk: The server security verdict is suspicious.

Mitigation: Review the skill before installing or using it, and apply the security guidance from the server evidence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chinmayagit/skills/webappbuilder)
- [Publisher profile](https://clawhub.ai/user/chinmayagit)
- [Default requirements](artifact/references/default-requirements.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration, markdown]

**Output Format:** [Markdown guidance with bash commands and generated project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated scaffold includes frontend and backend directories, environment examples, a starter README, API routes, and MVC backend modules.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
