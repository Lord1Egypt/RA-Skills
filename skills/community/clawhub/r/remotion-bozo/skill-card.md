## Description:

Creates Remotion video projects with a TypeScript project template, animation helpers, rendering scripts, Chrome reuse guidance, and Remotion best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bozoyan](https://clawhub.ai/user/bozoyan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and video engineers use this skill to scaffold Remotion projects, create reusable animation patterns, preview and render videos, and configure local or Lambda-based rendering workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated project paths may escape the intended folder when unsafe project names are used.

Mitigation: Use simple project names without slashes or special characters, review the resolved path, and run scaffolding only inside an empty or disposable parent directory.

Risk: Lambda rendering can rely on AWS credentials and may upload or delete cloud resources.

Mitigation: Use least-privilege or short-lived AWS credentials, avoid sensitive media unless uploads are understood, and review any Lambda or S3 resources before running deletion commands.

Risk: Project creation installs npm dependencies and writes package and source files into the generated project.

Mitigation: Review pinned package versions and generated files, then run dependency installation in an isolated workspace when evaluating the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bozoyan/skills/remotion-bozo)
- [Remotion Documentation](https://www.remotion.dev/docs)
- [Project Template Rules](rules/project-template.md)
- [Animation Tools Rules](rules/animation-tools.md)
- [Rendering Rules](rules/rendering.md)
- [Chrome Reuse Rules](rules/chrome-reuse.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, TypeScript examples, JSON configuration, and scaffolded project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Remotion project structure, npm scripts, animation snippets, browser configuration guidance, and local or Lambda rendering commands.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
