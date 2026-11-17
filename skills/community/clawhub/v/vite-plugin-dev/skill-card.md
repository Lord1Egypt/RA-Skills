## Description:

Use when developing Vite plugins: scaffolding plugin structure, implementing hooks such as transform, resolveId, load, and buildStart, handling virtual modules, HMR integration, SSR compatibility, and publishing to npm for the Vite 5 and 6 plugin API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goldath](https://clawhub.ai/user/goldath)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create, test, make SSR-compatible, and publish Vite plugins for Vite 5 and 6 projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Config injection examples can expose sensitive server-side values if secrets are included in Vite define or virtual modules.

Mitigation: Only pass explicitly public values into Vite define or virtual modules; exclude tokens, passwords, private endpoints, and server-only environment values.

## Reference(s):

- [Vite Plugin Hooks Reference](references/hooks-reference.md)
- [Vite Plugin Patterns & Examples](references/plugin-patterns.md)
- [Publishing a Vite Plugin to npm](references/publishing-guide.md)
- [ClawHub skill page](https://clawhub.ai/goldath/skills/vite-plugin-dev)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with TypeScript, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include implementation checklists and package configuration snippets.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
