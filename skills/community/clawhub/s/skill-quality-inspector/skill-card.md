## Description:

Audits skill repositories for quality, consistency, security, redundancy, and directory structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skills-repo](https://clawhub.ai/user/skills-repo)

### License/Terms of Use:

MIT

## Use Case:

Skill repository maintainers and review agents use this skill to check repositories against quality gates, find broken links and contradictions, assess security, maintenance, and compliance risks, compare overlapping skills, and prepare remediation reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation examples use unpinned sources with global installation and automatic confirmation.

Mitigation: Review and pin the intended release, and choose installation scope and confirmation deliberately.

Risk: Some organization-wide checks rely on separate skills-repo-admin tools and rules that are not included.

Mitigation: Review and run those checks separately before treating an organizational audit as complete.

Risk: Repair recommendations can change repository content or registry data.

Mitigation: Review the proposed changes and authorize them explicitly before applying repairs.

## Reference(s):

- [Quality dimensions and gates](references/quality-dimensions.md)
- [Contradiction detection](references/contradiction-detection.md)
- [Risk assessment](references/risk-assessment.md)
- [Redundancy reduction](references/redundancy-reduction.md)
- [Directory standardization](references/directory-standardization.md)
- [ClawHub release page](https://clawhub.ai/skills-repo/skills/skill-quality-inspector)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown]

**Output Format:** [Markdown reports and JSON scan findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Audits are read-only by default; proposed repairs require explicit authorization.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
