## Description:

Rebuilds reviewable README, FAQ, example, and consistency-risk documentation from a skill's SKILL.md, scripts, and resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this agent to audit a skill directory and draft README sections, FAQ entries, examples, missing-item notes, and consistency risks before release or maintenance updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill samples files from a user-provided directory, so reports may include private or sensitive local content if run on broad folders.

Mitigation: Use it on intended skill folders, avoid broad private directories, and review generated reports before sharing or writing them with --output.

Risk: Generated README, FAQ, examples, or consistency-risk notes can be misleading when source skill files are incomplete or stale.

Mitigation: Treat outputs as reviewable drafts and verify them against SKILL.md, scripts, resources, and release requirements before deployment.

Risk: The artifact primarily produces Chinese-language reports, which may limit reviewer understanding in non-Chinese review workflows.

Mitigation: Route outputs to reviewers who can read the language used, or translate and re-review before relying on the documentation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/skill-readme-rebuilder)
- [resources/spec.json](artifact/resources/spec.json)
- [resources/template.md](artifact/resources/template.md)
- [examples/example-input.md](artifact/examples/example-input.md)
- [examples/example-output.md](artifact/examples/example-output.md)

## Skill Output:

**Output Type(s):** [markdown, guidance, shell commands, configuration]

**Output Format:** [Markdown report by default, with an optional JSON wrapper from the local script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write reports to a requested output file; requires python3 and standard-library modules only.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
