## Description:

Unicon CLI helps agents add and manage icons in React, Vue, Svelte, and web projects using search, bundling, configuration, component generation, API usage, and format conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlesrhoward](https://clawhub.ai/user/charlesrhoward)

### License/Terms of Use:

MIT

## Use Case:

Developers and coding agents use this skill to select, configure, generate, and maintain project icons from the Unicon CLI and API. It supports icon search, bundle creation, framework-specific component output, project audits, cache management, and assistant integration guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or running mutable third-party npm code globally or through unpinned npx execution can introduce supply-chain risk in sensitive projects.

Mitigation: Review the npm package source, pin an exact trusted version, and avoid global or unpinned npx execution in sensitive projects.

Risk: Assistant integration commands such as unicon skill --all or --force can persistently overwrite assistant rule files.

Mitigation: Review the files the command will write and keep backups before using --all or --force.

Risk: API-returned SVG content is untrusted markup when rendered inside an application.

Mitigation: Sanitize API-returned SVG before rendering it and review any direct HTML injection patterns.

## Reference(s):

- [CLI Commands Reference](references/cli-commands.md)
- [Config File Reference](references/config-file.md)
- [API Reference](references/api-reference.md)
- [Unicon Website](https://unicon.sh)
- [Unicon API](https://unicon.sh/api)
- [Unicon Config Schema](https://unicon.sh/schema/uniconrc.json)
- [Unicon Repository](https://github.com/WebRenew/unicon)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and generated code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce project files such as icon components, SVG or JSON icon data, .uniconrc.json configuration, and assistant rule files when the documented CLI commands are executed.]

## Skill Version(s):

0.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
