## Description:

Scans repository directories and documentation to generate onboarding paths, recommended reading order, and common pitfalls for new team members.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to create repository onboarding guides for new contributors, including repository overview, reading order, key directories, setup preparation, common pitfalls, and documentation gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner can follow symlinks and may read files outside the intended repository.

Mitigation: Run it only on trusted repository trees, prefer dry-run or stdout review, and add symlink containment and file-size limits before broader deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/repo-onboarding-guide)
- [Publisher profile](https://clawhub.ai/user/52yuanchangxing)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or JSON reports; may include reviewed shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write to stdout or an output file; dry-run mode is available.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
