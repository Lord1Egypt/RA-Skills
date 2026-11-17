## Description:

Analyzes and optimizes Agent Skills by monitoring usage, assessing health, checking code quality, generating improvement suggestions, and exporting reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to monitor OpenClaw Agent Skill usage, evaluate health and code quality, collect feedback, and generate JSON, Markdown, or HTML reports with improvement recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Malformed skill names or directories may make the tool inspect unintended local folders.

Mitigation: Run it only on trusted skill names and directories, and review paths before analyzing or clearing data.

Risk: Usage context, errors, comments, and user IDs are stored in a persistent local SQLite database.

Mitigation: Avoid putting secrets, personal data, or sensitive operational details into monitored context, error messages, comments, or user identifiers.

Risk: Exported HTML reports may be unsafe when generated from untrusted inputs.

Mitigation: Avoid opening HTML reports from untrusted skill inputs until HTML escaping and path validation issues are fixed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/skills/skill-auto-evolver)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands, Python API examples, and report outputs in JSON, Markdown, or HTML.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores local usage, health, and feedback records in SQLite and can export skill health reports.]

## Skill Version(s):

0.1.2 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
