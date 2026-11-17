## Description:

Validate JSON-exported webpack configuration files for structural issues, deprecated loaders/plugins, optimization gaps, and best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit JSON-exported webpack configurations before production builds or CI enforcement. It highlights structural errors, deprecated loaders and plugins, optimization gaps, and best-practice issues, and can propose concrete configuration fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exporting a webpack.config.js through Node can execute code from the target project.

Mitigation: Run the export command only in trusted project workspaces; pass the validator a JSON-exported config file rather than the JavaScript config itself.

Risk: Static configuration checks can miss project-specific build behavior or produce findings that need judgment.

Mitigation: Review validation output before changing build settings, and confirm changes with the project's normal webpack build and CI tests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/webpack-config-validator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text, summary text, or JSON findings with optional suggested configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI-style validation output may include errors, warnings, informational findings, exit codes, and fix suggestions.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata, created 2026-05-01)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
