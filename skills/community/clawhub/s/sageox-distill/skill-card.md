## Description:

Syncs, indexes, and distills team activity across SageOx-enabled repositories so a team's knowledge base stays current with repository context and GitHub activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galexy](https://clawhub.ai/user/galexy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and team maintainers use this skill to keep SageOx-enabled repository knowledge current by syncing team context, indexing GitHub PRs, issues, and comments, and running daily distillation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow requires local installation and authentication for SageOx, GitHub, and Claude tooling.

Mitigation: Install only when those tools are intended for the selected repositories, authenticate the CLIs deliberately, and use reviewed skill releases for ox reinstallations.

Risk: The workflow indexes GitHub activity and runs distillation through SageOx and Claude.

Mitigation: Use it only for repositories and teams where that data processing is acceptable, and confirm credentials before running the distillation pipeline.

Risk: The ox CLI is downloaded as a remote release archive during the install flow.

Mitigation: Use the bundled pinned-release installer, which checks a fixed tag and per-platform SHA-256 values, and avoid unsupported package-manager installs inside the skill.

Risk: Repository paths and saved manifest values can be user-modified before a run.

Mitigation: Validate absolute paths, reject parent-directory segments and shell metacharacters, and re-validate manifest values before using them.

## Reference(s):

- [SageOx](https://sageox.ai)
- [SageOx Summary skill](https://clawhub.ai/skills/sageox-summary)
- [Installing ox](references/INSTALL.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text status lines with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A successful run may produce only a concise team status line such as all ok.]

## Skill Version(s):

0.2.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
