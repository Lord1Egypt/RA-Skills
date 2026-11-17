## Description:

Audits installed skills for trigger overlaps, uncovered tasks, weak descriptions, duplicates, and unnecessary loading cost, then produces a health report with prioritized fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thomaszhou22](https://clawhub.ai/user/thomaszhou22)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to review an installed skill collection for conflicting or missing triggers, weak descriptions, duplicates, and unused loading cost. It returns a health report with prioritized description improvements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was partial because two referenced memory paths could not be resolved, so the report may miss relevant state.

Mitigation: Check the referenced paths and review the relevant skill files before relying on the report.

Risk: The scan reads installed skill files, and first-use setup stores configuration in a memory state file.

Mitigation: Confirm the skills directory is the intended one and keep the setup state file in the intended project.

## Reference(s):

- [Health Report Template](artifact/references/report-template.md)
- [ClawHub Release Page](https://clawhub.ai/thomaszhou22/skills/skill-health-scan)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown health report with tables and prioritized suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include trigger overlap findings, dead-zone ideas, description rewrites, duplicate and bloat findings, and suggested fixes.]

## Skill Version(s):

1.1.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
