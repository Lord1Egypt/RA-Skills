## Description:

Semantic git history search and code archaeology. Use when asked why code exists, who owns a file, what introduced a regression, what changed in a commit range, or whether a change is risky to revert.

This skill is ready for commercial/non-commercial use.

## Publisher:

[venki0552](https://clawhub.ai/user/venki0552)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to investigate git history with the local slg CLI, including code rationale, ownership, regression origins, commit history, diff summaries, and revert risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and can run an unpinned npm package.

Mitigation: Review the package before use, pin the slg-cli version, and prefer a project-local or sandboxed install over a global install.

Risk: The CLI indexes repository git history, which may include sensitive material.

Mitigation: Avoid indexing repositories whose history contains sensitive data unless a local semantic index is acceptable for that environment.

## Reference(s):

- [slg-cli homepage](https://github.com/vrknetha/slg-cli)
- [ClawHub skill page](https://clawhub.ai/venki0552/skills/slg-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe local CLI commands and MCP server configuration for repository history analysis.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
