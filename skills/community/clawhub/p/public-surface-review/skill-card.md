## Description:

Publish Guard audits a repository's public release surface, including README, SKILL.md, agent metadata, launch docs, and obvious leak patterns before GitHub or ClawHub publication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release maintainers use Publish Guard before publishing GitHub repositories or ClawHub skills to find public-audience issues, weak first-run copy, internal launch material, and obvious leak patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanners may follow repository symlinks and read user-readable files outside the intended target repository.

Mitigation: Run the skill only on trusted repositories or in an isolated workspace until symlink containment is fixed.

Risk: Local audit reports may include limited findings or snippets derived from files reached through crafted repository paths.

Mitigation: Review generated reports before sharing them and avoid running the skill against untrusted working trees.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zack-dev-cm/skills/public-surface-review)
- [Publisher Homepage](https://zack-dev-cm.github.io/)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown audit with supporting JSON scanner outputs and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes leak findings, public-surface findings, launch-copy score, and a publish recommendation.]

## Skill Version(s):

1.0.5 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
