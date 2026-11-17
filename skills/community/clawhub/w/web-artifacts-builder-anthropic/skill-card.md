## Description:

Builds complex Claude.ai HTML artifacts with React, TypeScript, Tailwind CSS, Vite, Parcel, and shadcn/ui.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pupuking723](https://clawhub.ai/user/pupuking723)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and agents use this skill to initialize a modern React artifact project, build a multi-component frontend, and bundle it into a single HTML file for Claude.ai artifact sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs local shell scripts that create project files and install JavaScript dependencies.

Mitigation: Run it in a disposable workspace or container, avoid elevated privileges, inspect scripts before execution, and pin dependencies or use a lockfile for repeatable builds.

Risk: Initialization may fail if the referenced shadcn-components.tar.gz archive is not present.

Mitigation: Confirm the package includes the archive before running initialization, or supply the missing archive through an approved source.

## Reference(s):

- [shadcn/ui Components](https://ui.shadcn.com/docs/components)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown guidance with bash commands plus generated project files and a single-file HTML artifact.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18 or newer, pnpm, and an available shadcn-components.tar.gz archive for initialization.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
