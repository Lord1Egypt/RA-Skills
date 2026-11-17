## Description:

Checks skill directories before installation by reviewing declared binaries, environment variables, configuration, operating system, and sandbox requirements, then explains compatibility gaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to review whether an OpenClaw skill directory appears ready to install on a target machine, with attention to missing dependencies, OS and sandbox concerns, configuration gaps, installation advice, and rollback advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can explain installation readiness, but evidence says it does not fully verify OS state, environment variables, sandbox conditions, or installed binaries beyond its python3 requirement.

Mitigation: Treat the report as a review aid and confirm machine-specific dependencies and sandbox constraints separately before installation.

Risk: Input may contain sensitive machine, project, or skill details.

Mitigation: Use local, sanitized inputs where practical and review generated Markdown before sharing it.

Risk: The local helper can write a report file when an output path is supplied.

Mitigation: Omit --output or use --dry-run when a read-only review is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/skill-install-checker)
- [README](artifact/README.md)
- [Specification](artifact/resources/spec.json)
- [Output template](artifact/resources/template.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration guidance, shell commands]

**Output Format:** [Markdown report, with optional JSON wrapping when the local script is run with --format json]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report is generated from local input and may include environment overview, missing dependencies, OS and sandbox risks, configuration gaps, installation advice, rollback advice, pending questions, and next steps.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
