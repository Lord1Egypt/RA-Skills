## Description:

Helps agents work with Statamic CMS content structure, collections, blueprints, fieldsets, Bard YAML content, globals, taxonomies, navigation, forms, assets, and addon development patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michael-stokoe](https://clawhub.ai/user/michael-stokoe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content teams use this skill to guide agents when authoring or editing Statamic CMS content files, field definitions, and addon scaffolding. It is most useful for producing YAML examples, PHP/Laravel addon code patterns, shell commands, and configuration guidance within existing Statamic projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated composer, pnpm, artisan, or build-cleanup commands may change dependencies, caches, generated assets, or project state when run in a real Statamic project.

Mitigation: Review commands before execution, run them in the intended project directory, and use version control or a disposable environment for dependency and build changes.

Risk: Generated Statamic YAML, PHP, route, middleware, or authorization examples may not match a project's existing content model or access-control requirements.

Mitigation: Validate generated files against the project's blueprints, permissions, and tests before deployment.

## Reference(s):

- [Statamic Development artifact](artifact/SKILL.md)
- [ClawHub skill page](https://clawhub.ai/michael-stokoe/skills/statamic-dev)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with YAML, PHP, JavaScript, JSON, XML, Antlers, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are advisory and should be reviewed before applying generated commands or code in a real Statamic project.]

## Skill Version(s):

0.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
