## Description:

Skill Subtraction checks installed AI skills across agent platforms and produces bilingual keep, archive, or uninstall recommendations from bounded skill metadata, scoring rules, duplicate detection, and archive inventory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[helloyxs](https://clawhub.ai/user/helloyxs)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to inventory installed skills, identify stale or overlapping skills, and decide what to keep, archive, or uninstall. It is intended for skill-set maintenance workflows where cleanup decisions are reviewed before changes are made.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill inventories local agent skill directories and may surface local skill metadata in its reports.

Mitigation: Install and run it only when that inventorying is acceptable, and review reports before sharing them.

Risk: Archive or uninstall recommendations could affect skills the user still needs.

Mitigation: Review the proposed cleanup plan and approve only the specific archive or uninstall actions that should proceed.

Risk: Recommendations are based on bounded metadata and scoring rules, so they may miss context about how a skill is actually used.

Mitigation: Treat recommendations as decision support and confirm high-value or project-specific skills before cleanup.

## Reference(s):

- [Evaluation Framework](references/evaluation_framework.md)
- [Example Reports](examples/README.md)
- [ClawHub Skill Page](https://clawhub.ai/helloyxs/skills/skill-subtraction)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown reports with structured recommendation tables and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports Chinese and English output; cleanup actions require explicit user confirmation.]

## Skill Version(s):

1.1.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
