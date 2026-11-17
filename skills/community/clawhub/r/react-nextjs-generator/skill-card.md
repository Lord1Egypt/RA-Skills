## Description:

Generates complete React Next.js projects from requirements and UI designs using Ant Design, Tailwind CSS, and Zustand for state management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[batype](https://clawhub.ai/user/batype)

### License/Terms of Use:


## Use Case:

Developers use this skill to turn requirement documents and optional UI design inputs into a starter React and Next.js application with pages, components, state management, styling, and project configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to run local scripts and generate files from user-provided text without enough path, dependency, or code-injection safeguards.

Mitigation: Run the skill in a disposable workspace, verify the invoked script path points to the installed artifact, and review generated files before installing dependencies or running the application.

Risk: Untrusted requirement documents or UI inputs could influence generated code and project configuration.

Mitigation: Avoid untrusted inputs when possible and inspect generated pages, components, package scripts, and configuration before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/batype/skills/react-nextjs-generator)
- [Publisher profile](https://clawhub.ai/user/batype)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with generated project files, TypeScript and TSX source code, JSON configuration, CSS, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a Next.js project structure with package configuration, app pages, reusable components, Zustand stores, Tailwind configuration, and instructions for installing dependencies and running the development server.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
