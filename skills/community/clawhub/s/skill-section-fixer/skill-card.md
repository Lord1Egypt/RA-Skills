## Description:

Skill Section Fixer repairs missing required sections and frontmatter fields in SKILL.md files, including batch repair for skill directories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xukaitai321300-ctrl](https://clawhub.ai/user/xukaitai321300-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to make WorkBuddy or ClawHub skill packages pass structural checks by adding missing SKILL.md sections and frontmatter fields. It is most useful for controlled maintenance of local skill directories before review or testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can rewrite many installed SKILL.md files in place, especially when batch mode is used.

Mitigation: Run dry-run first, use exact target paths, keep backups or version control, and review generated frontmatter and sections before accepting changes.

Risk: Batch behavior is under-scoped and may touch more local skills than intended.

Mitigation: Avoid broad batch mode unless the target directory has been reviewed and use the maximum-count option where appropriate.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Python command examples and in-place file updates when executed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can run in dry-run mode for preview; batch mode may update multiple SKILL.md files.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
