## Description:

Security compliance checker for MCP/LLM applications. Performs non-invasive security assessments on configuration files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaillera999](https://clawhub.ai/user/kaillera999)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use SafeClaw to check MCP/LLM application configuration files for secrets, permissions, network exposure, plugin-source issues, logging and audit gaps, version exposure, and OpenClaw deployment settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill invokes checker code outside the reviewed artifact.

Mitigation: Review and trust the referenced workspace checker implementation before invocation, and pin its dependencies.

Risk: A user-provided configuration path is used in a shell-shaped command.

Mitigation: Run only in controlled workspaces, quote paths carefully, avoid untrusted path input, and narrow filesystem scope.

Risk: Example MCP server entries include package launch commands and broad filesystem access.

Mitigation: Do not copy example server entries directly without pinning package versions and restricting filesystem paths to required directories.

## Reference(s):

- [SafeClaw ClawHub Release](https://clawhub.ai/kaillera999/skills/safeclaw)
- [SafeClaw README](artifact/README.md)
- [Example Configuration](artifact/example-config.json)
- [Minimal Configuration Template](artifact/templates/minimal-config.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report summarizing JSON check results with prioritized findings and remediation steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exit codes distinguish pass, attention, and high-risk findings; JSON, YAML, and TOML configuration inputs are supported.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
