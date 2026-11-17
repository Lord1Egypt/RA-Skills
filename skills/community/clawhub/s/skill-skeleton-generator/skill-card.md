## Description:

Generates starter SKILL.md and AGENTS.md files with frontmatter from a single command.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers creating AI skills use it to scaffold SKILL.md and AGENTS.md files with standardized frontmatter and starter sections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generator can overwrite existing agent instruction files and does not enforce its advertised directory-containment or symlink safeguards.

Mitigation: Use a new, empty directory inside a restricted workspace, avoid symlinked destinations, and back up existing instruction files; prefer a revision that enforces containment, rejects symlinks, and refuses overwrites.

## Reference(s):

- [LGD Hub](https://zhaoxinghua09-cell.github.io/lgd-hub/)
- [ClawHub release page](https://clawhub.ai/zhaoxinghua09-cell/skills/skill-skeleton-generator)

## Skill Output:

**Output Type(s):** [Files, Markdown]

**Output Format:** [SKILL.md and AGENTS.md files with YAML frontmatter and editable starter sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated capability and verification sections contain placeholder text that requires human editing.]

## Skill Version(s):

1.0.7 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
