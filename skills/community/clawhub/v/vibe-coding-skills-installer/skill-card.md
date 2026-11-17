## Description:

Install vibe coding skill sets (openspec, gstack, superpowers) for supported agent platforms including Cursor, Claude Code, Codex, Windsurf, Gemini CLI, and OpenCode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fdingiit](https://clawhub.ai/user/fdingiit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install and configure OpenSpec, gstack, and Superpowers skill sets across supported coding-agent platforms. It helps choose platform-specific paths, install scope, prerequisites, execution steps, and post-install verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can modify user-level or project-level agent skill directories.

Mitigation: Review the target platform and install scope before execution, and prefer project-level installation when possible.

Risk: The installer can fetch and run unpinned third-party code from npm and GitHub repositories.

Mitigation: Ask the agent to show exact commands, target directories, repository commits or package versions, and rollback steps before proceeding.

Risk: Global installation can affect multiple projects on the same machine.

Mitigation: Use project scope for repository-specific workflows unless a shared global install is explicitly needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fdingiit/skills/vibe-coding-skills-installer)
- [Platform reference](platforms.md)
- [OpenSpec workflow skills](https://github.com/samotage/cursor-openspec-workflows)
- [gstack](https://github.com/garrytan/gstack)
- [Superpowers](https://github.com/obra/superpowers)
- [Superpowers OpenCode install guide](https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/.opencode/INSTALL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and summary tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask interactive questions before proposing or running platform-specific install and verification commands.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
