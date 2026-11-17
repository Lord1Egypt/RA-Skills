## Description:

Workspace Git Setup helps agents initialize or audit local Git tracking with a security-focused .gitignore, large-file warnings, and dry-run or audit modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songhonglei](https://clawhub.ai/user/songhonglei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to add local Git version tracking to a workspace or run a read-only repository health audit. It is useful for setting a baseline .gitignore, checking for tracked sensitive files, spotting untracked files, and previewing setup changes before applying them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The README shows a mutable main-branch curl command for obtaining the setup script.

Mitigation: Install from a pinned repository revision or audited package before running the script.

Risk: The default setup path stages and commits every unignored file in the selected workspace.

Mitigation: Run --dry-run or --audit first, confirm the workspace path, and inspect the files that would be committed.

Risk: Normal setup can change local Git configuration and write or replace .gitignore rules.

Mitigation: Review the proposed .gitignore diff and use audit mode when only repository health information is needed.

## Reference(s):

- [Workspace Git Setup on ClawHub](https://clawhub.ai/songhonglei/skills/workspace-git-setup)
- [Declared source repository in artifact](https://github.com/Songhonglei/better-agent-skills)
- [Git installation documentation](https://git-scm.com/downloads)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and local Git configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce commands that mutate local Git state unless audit or dry-run mode is used.]

## Skill Version(s):

1.0.3 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
