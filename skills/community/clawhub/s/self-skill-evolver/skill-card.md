## Description:

Analyzes OpenClaw agent skills by tracking usage, checking health and code quality, and generating improvement recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this CLI to evaluate OpenClaw skill reliability, performance, maintainability, and release readiness. It supports local analysis, usage logging, feedback capture, health scoring, and JSON, Markdown, or HTML reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The tool scans local skill paths and may inspect broader local files than intended.

Mitigation: Run it only against trusted skill names and explicit paths that are appropriate to analyze.

Risk: Usage context, errors, and feedback can be stored in a SQLite database in the user's home directory.

Mitigation: Avoid logging sensitive context, secrets, or raw error details, and periodically clear old telemetry.

Risk: HTML reports may render untrusted skill names or recommendations.

Mitigation: Treat generated HTML as untrusted content and review or sanitize report inputs before sharing or opening in sensitive environments.

## Reference(s):

- [Self Skill Evolver README](README.md)
- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/skills/self-skill-evolver)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [CLI text plus JSON, Markdown, or HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write report files and local SQLite skill-usage records.]

## Skill Version(s):

0.1.2 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
