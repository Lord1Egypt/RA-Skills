## Description:

Generates TypeScript configuration for strict, React, Node.js, minimal, and library project scenarios.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunshine-del-ux](https://clawhub.ai/user/sunshine-del-ux)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to create a TypeScript tsconfig.json for common project setups such as strict mode, Node.js services, React applications, prototypes, and libraries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generator creates or overwrites tsconfig.json in the current project directory.

Mitigation: Run it only in a project where creating or replacing tsconfig.json is intended, and review existing configuration before execution.

Risk: The documentation suggests a global TypeScript installation as part of setup.

Mitigation: Approve development-environment changes before running global package installation commands.

Risk: The primary documentation is in Chinese, which may lead to missed usage details for readers who do not read Chinese.

Mitigation: Review or translate the documentation before using the skill in a project workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunshine-del-ux/skills/typescript-config-generator)

## Skill Output:

**Output Type(s):** [Configuration, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell command examples and generated JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script writes tsconfig.json in the current working directory.]

## Skill Version(s):

1.0.0 (source: artifact/_meta.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
