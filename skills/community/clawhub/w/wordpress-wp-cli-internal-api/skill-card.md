## Description:

Build, inspect, and extend WP-CLI command code using the documented stable internal API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matthewxmurphy](https://clawhub.ai/user/matthewxmurphy)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to build or review custom WP-CLI command code that relies on documented stable internal APIs for command registration, hooks, output helpers, and internal execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional skeleton generator can produce PHP from user-supplied command and class names.

Mitigation: Pass only trusted, simple command and class names, then review generated PHP before loading it in a WordPress or WP-CLI environment.

Risk: Generated command guidance may be applied to destructive WP-CLI workflows.

Mitigation: Use WP-CLI confirmation patterns, print the action scope before execution, and review command behavior before deployment.

## Reference(s):

- [Stable Internal API](references/stable-internal-api.md)
- [Command Patterns](references/command-patterns.md)
- [WP-CLI Internal API Reference](https://make.wordpress.org/cli/handbook/references/internal-api/)
- [ClawHub Skill Page](https://clawhub.ai/matthewxmurphy/skills/wordpress-wp-cli-internal-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with PHP code examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May render a local PHP command skeleton for review before use in WordPress or WP-CLI environments.]

## Skill Version(s):

0.5.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
