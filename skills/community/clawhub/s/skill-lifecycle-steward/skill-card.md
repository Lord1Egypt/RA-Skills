## Description:

A unified skill lifecycle steward that handles discovery, evaluation, installation, upgrade, and removal of skills. Use when the user wants to find, recommend, install, enable, inspect, upgrade, or uninstall a skill, or assess a candidate skill's quality and safety.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhaisong](https://clawhub.ai/user/huhaisong)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to help users discover and assess skills, install or enable a chosen skill, inspect installed skills, and manage upgrades, edits, or removal with confirmation and safety checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requirement-based searches may send user requirements to third parties.

Mitigation: Review the search scope and avoid including sensitive requirements in external searches.

Risk: The security scan was partial because a referenced path was missing, so related behavior was not fully reviewed.

Mitigation: Review the available skill files and confirm the target and installation path before installing a skill.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huhaisong/skills/skill-lifecycle-steward)
- [Evaluation guide](references/evaluation-guide.md)
- [Security scan guide](references/security-scan.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown]

**Output Format:** [Structured Markdown recommendations, status summaries, and action checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include skill sources, ratings, trigger terms, installation methods, and change summaries.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
