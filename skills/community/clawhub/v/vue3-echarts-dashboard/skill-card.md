## Description:

Generates Vue3, TypeScript, and ECharts dashboard projects or injects reusable chart components into existing Vue3 applications using shared builder, hook, and component assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liyumingben](https://clawhub.ai/user/liyumingben)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to scaffold a Vue3 visual dashboard or add a single ECharts chart component to an existing Vue3 project. It is suited for data dashboards, large-screen visualizations, and reusable chart component generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes files into a target Vue project and supports overwrite behavior.

Mitigation: Run dry-run first, inspect the planned target path, and use overwrite options only after reviewing existing project files.

Risk: Generated dashboard projects may introduce npm dependencies that affect production security and maintenance posture.

Mitigation: Audit and pin dependencies before production use, especially optional ECharts plugin packages and UI/runtime libraries.

Risk: Map visualizations can carry geographic-data compliance obligations.

Mitigation: Review the bundled or replacement geoJSON source and use approved standard map data for production deployments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liyumingben/skills/vue3-echarts-dashboard)
- [ECharts option documentation](https://echarts.apache.org/zh/option.html)
- [Chart option cookbook](references/chart-option-cookbook.md)
- [Conventions and integration notes](references/conventions.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated Vue, TypeScript, JSON, and configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write project files, chart component files, hooks, builders, sample data, and optional dependency installation commands.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
