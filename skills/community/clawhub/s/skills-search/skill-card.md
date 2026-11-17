## Description:

Search skills.sh registry from CLI. Find and discover agent skills from the skills.sh ecosystem.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thesethrose](https://clawhub.ai/user/thesethrose)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to search the skills.sh registry from a terminal, inspect popular skills, and generate install commands for selected registry results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search results and generated install commands can lead users to third-party skill sources.

Mitigation: Review the discovered skill source and confirm the repository or publisher is trusted before installing.

Risk: Terminal-generated install commands can introduce supply-chain risk if copied without review.

Mitigation: Prefer pinned package versions where possible and do not run install commands unless the repository name looks valid and trusted.

## Reference(s):

- [ClawHub Skills.sh Search release page](https://clawhub.ai/thesethrose/skills/skills-search)
- [skills.sh](https://skills.sh)
- [skills.sh API endpoint](https://skills.sh/api/skills)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Terminal text with optional inline install commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results are sorted by install count and may include generated skills CLI install commands when requested.]

## Skill Version(s):

1.0.4 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
