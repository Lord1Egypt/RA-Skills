## Description:

Workspace Bootstrap helps agents and users quickly create an OpenClaw workspace structure, core file templates, example configurations, and workspace pitfall checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jack-long-2022](https://clawhub.ai/user/jack-long-2022)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to bootstrap a workspace with standard directories, core Markdown files, scenario examples, and validation scripts. It is useful for first-time setup, recreating an existing workspace layout, or checking a workspace for common configuration problems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bootstrap or wizard scripts can overwrite existing workspace files.

Mitigation: Run them in a new empty directory or back up the target workspace before execution, then review generated files.

Risk: Workspace documentation may lead users to store sensitive data in plaintext workspace files.

Mitigation: Avoid storing secrets in TOOLS.md or user-data/apis, and review private workspace data before sharing or committing files.

Risk: Generated or copied workspace data may accidentally be published.

Mitigation: Review files before using broad git commands, exclude private user-data, and avoid committing unreviewed generated content.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jack-long-2022/skills/workspace-bootstrap)
- [Quickstart Guide](docs/QUICKSTART.md)
- [Usage Guide](docs/USAGE.md)
- [Workspace Template](templates/WORKSPACE-TEMPLATE.md)
- [Workspace Examples](templates/WORKSPACE-EXAMPLES.md)
- [Test Report](tests/test-report.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command snippets and generated workspace template files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes reusable workspace templates, example configurations, bootstrap scripts, a setup wizard, validation scripts, and pitfall checks.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md, README.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
