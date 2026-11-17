## Description:

Audit a target SKILL.md against the Agent Skills specification and generate a Chinese HTML report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oahc09](https://clawhub.ai/user/oahc09)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to audit SKILL.md files before sharing or publishing them. It checks specification fields, semantic quality, and execution guidance, then reports severe findings, warnings, and suggested fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The checker uses strict heuristics, so findings may not always be definitive specification truth.

Mitigation: Use the HTML report as an audit aid and manually review severe and warning findings before changing or publishing a skill.

Risk: The checker reads the target SKILL.md path provided by the user and writes an HTML report.

Mitigation: Confirm the target path and output report path before running the generated command, especially when auditing files outside the current workspace.

Risk: Generated reports can contain excerpts from the audited skill file.

Mitigation: Review reports before sharing them and avoid publishing reports that include sensitive local content.

## Reference(s):

- [Skill Checker Specification Checklist](artifact/references/specification-checklist.md)
- [ClawHub Skill Page](https://clawhub.ai/oahc09/skills/skill-checker)

## Skill Output:

**Output Type(s):** [text, files, shell commands, guidance]

**Output Format:** [Text summary and static HTML report file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report includes pass/fail status, severe finding count, warning count, localized findings, and suggested fixes.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact metadata reports 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
