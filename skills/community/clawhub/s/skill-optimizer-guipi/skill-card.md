## Description:

A WorkBuddy skill that helps agents modify and optimize existing skills by diagnosing workflow gaps, logic errors, rule changes, and lessons learned.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guipi888](https://clawhub.ai/user/guipi888)

### License/Terms of Use:

MIT

## Use Case:

Developers and skill maintainers use this skill to update WorkBuddy skills with minimal edits, version records, and accumulated lessons from observed failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently modify other installed skills, so accidental activation or broad approval could change future agent behavior.

Mitigation: Require the agent to name target files, show a diff, and get explicit approval before writing changes.

Risk: Skill edits can introduce incorrect or misleading guidance into future runs.

Mitigation: Review and scan modified skills before deployment.

Risk: Broad trigger phrases can activate the skill when the user intended discussion rather than file modification.

Mitigation: Narrow activation triggers or require an explicit confirmation step before entering the write workflow.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/guipi888/skills/skill-optimizer-guipi)
- [修改规范](references/修改规范.md)
- [优化经验](references/优化经验.md)
- [踩坑总库](references/踩坑总库.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and file-change instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May result in edits to SKILL.md and references/pitfalls.md when an agent is allowed to write files.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
