## Description:

Debloats bloated, flaky Agent Skills by classifying content across WHAT, WHERE, HOW, and ALIVE axes, using local analysis scripts and user-confirmed deletion gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liyi-ai](https://clawhub.ai/user/liyi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to audit, reorganize, and slim down Agent Skills that have become long, stale, or inconsistent. It produces analysis and proposed changes while requiring explicit user confirmation before any deletion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic reorganization could move important skill guidance into a less-visible layer and make agent behavior less reliable.

Mitigation: Review proposed reorganizations and verify the debloated skill against representative tasks before deployment.

Risk: Deleting stale-looking files can permanently remove information that is still useful to the skill owner.

Mitigation: Approve deletions only after confirming a backup exists and the listed files are truly stale; default to keeping uncertain items.

Risk: Generated guidance could introduce incorrect or misleading changes into a target skill.

Mitigation: Review and scan the modified skill before release or installation.

## Reference(s):

- [Skill Debloater ClawHub page](https://clawhub.ai/liyi-ai/skills/skill-debloater)
- [Four-Axis Debloating Methodology](artifact/references/methodology.md)
- [Interaction and Verification Templates](artifact/references/interaction-and-verify.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, analysis summaries, and proposed file or code changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local script outputs, before/after summaries, user-confirmation prompts for deletion, and verification notes.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
