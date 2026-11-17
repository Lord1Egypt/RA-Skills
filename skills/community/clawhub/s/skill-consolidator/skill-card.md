## Description:

Skill Consolidator scans installed AI agent skills, rules, and commands to detect name collisions, functional overlap, trigger conflicts, and version differences, then produces cleanup reports and categorized indexes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alancouny](https://clawhub.ai/user/alancouny)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to inventory local AI agent skills, identify duplicates or conflicts, and prepare reviewed cleanup or consolidation actions before installing or reorganizing skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local AI-agent skill and rule files across multiple configured directories and writes a local report.

Mitigation: Install only when that local scan scope is acceptable, use the review-only or no-write option when appropriate, and review generated reports before sharing them.

Risk: Cleanup or consolidation actions could disable, overwrite, or reorganize useful local skills if applied without review.

Mitigation: Treat scan output as recommendations first and confirm affected paths before allowing any cleanup or consolidation changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alancouny/skills/skill-consolidator)
- [Server-resolved source path](https://github.com/alancouny/skill-consolidator/tree/main/skill-consolidator)
- [Project homepage](https://github.com/alancouny/skill-consolidator)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration guidance]

**Output Format:** [Markdown report, optional JSON report, and concise guidance with shell commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js for the bundled scanner; reports are written locally unless no-write mode is used.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter and bundled scripts report 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
