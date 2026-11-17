## Description:

Audits installed WorkBuddy skills to identify duplicates, platform-mismatched skills, and maintenance candidates, then generates a structured cleanup report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderszhan](https://clawhub.ai/user/anderszhan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to audit installed WorkBuddy skills, compare them against an approved golden list, and identify unknown or platform-specific skills that need review before cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documentation includes an irreversible removal command for installed skill folders.

Mitigation: Use the skill for report generation first, manually verify exact absolute paths, and prefer moving candidates to a quarantine folder before deletion.

Risk: Unknown and platform-specific classifications can be incomplete or wrong because they depend on the golden list and keyword matching.

Mitigation: Review the generated report and golden list before taking cleanup action, especially for skills flagged as unknown or platform-specific.

## Reference(s):

- [Golden List - Authorized Skills Reference](references/golden-list.md)
- [ClawHub Skill Page](https://clawhub.ai/anderszhan/skills/workbuddy-skills-audit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with summary tables and cleanup recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates a dated skills-audit report; cleanup commands require user confirmation before use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
