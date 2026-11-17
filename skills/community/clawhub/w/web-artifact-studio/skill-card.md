## Description:

Web Artifact Studio guides agents in building interactive React web artifacts such as dashboards, form workflows, single-page app prototypes, component previews, and clickable demonstrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and product teams use this skill to ask an agent for interactive front-end artifacts, including dashboards, multi-step forms, SPA prototypes, component showcases, and demos built with React, TypeScript, Tailwind, shadcn/ui, and related tooling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential and API-key handling is inconsistent in the evidence.

Mitigation: Use the skill only under supervision, do not provide credentials to generated artifacts unless the target service has been separately verified, and store required secrets in environment variables.

Risk: Generated workflows may include package installation, build, or other shell commands.

Mitigation: Review commands before execution and run npm, Vite, and related tooling in a sandboxed project with least-privilege filesystem access.

Risk: Generated artifacts may persist data in browser localStorage.

Mitigation: Avoid storing real personal, confidential, or regulated data in localStorage; use mock data or an approved storage design for sensitive workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/web-artifact-studio)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code blocks, shell commands, configuration snippets, and generated front-end project structure]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce React, TypeScript, Tailwind, shadcn/ui, Vite, routing, state-management, and single-file packaging guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
