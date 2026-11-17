## Description:

Web构件工作室 helps agents build interactive React web artifacts such as dashboards, form workflows, single-page app prototypes, component showcases, and clickable demos using TypeScript, Tailwind CSS, and shadcn/ui.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and product teams use this skill to turn frontend requirements into web artifact plans, React/TypeScript code, project files, configuration, and build commands for prototypes, dashboards, forms, component previews, and interactive demos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated frontend work may include npm, npx, Vite, dependency, or external API steps that affect the workspace.

Mitigation: Keep generated files scoped to the intended project directory and review commands, packages, and external API steps before running them.

Risk: Client-side artifacts can expose secrets or store real personal data unsafely if requirements ask for those patterns.

Mitigation: Do not hard-code API keys in client-side code, and avoid storing real personal data such as phone numbers or email addresses in localStorage without notice, retention limits, and a clear way to clear it.

Risk: Generated UI and code may require verification before reuse beyond prototype workflows.

Mitigation: Test build output, browser behavior, responsiveness, accessibility, and generated data handling before deployment or sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/web-artifact-studio-cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with code blocks, file plans, and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate frontend project files and local build instructions; review generated commands before execution.]

## Skill Version(s):

1.0.0 (source: server release evidence; artifact frontmatter lists 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
