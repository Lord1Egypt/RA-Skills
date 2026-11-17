## Description:

Generates Webpack and Vite configuration guidance for plugins, loaders, optimization, code splitting, and migrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to quickly produce build-tool configuration, command guidance, and generated webpack.config.js content for JavaScript projects and automation pipelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated webpack.config.js content can embed unsafe user-supplied values into executable JavaScript configuration.

Mitigation: Use only trusted, simple arguments and inspect generated webpack.config.js files before running webpack.

Risk: Untrusted project metadata or user input in options such as --entry, --output, or --port may create unsafe or misleading configuration.

Mitigation: Avoid populating generator options from untrusted input in automation.

## Reference(s):

- [Webpack Config on ClawHub](https://clawhub.ai/bytesagain3/skills/webpack-config)
- [BytesAgain Homepage](https://bytesagain.com)
- [Source Link from Skill Metadata](https://github.com/bytesagain/ai-skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and shell output with generated JavaScript configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate executable webpack.config.js content based on command-line options.]

## Skill Version(s):

2.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
