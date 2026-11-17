## Description:

Windows Shell gives agents practical command-line guidance for Windows 10/11 environments, including shell selection, Git Bash defaults, GBK/UTF-8 encoding, BOM handling, MSYS2 path rewriting, PowerShell and WSL routing, Python/Node.js execution, Git configuration, and code-generation practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenmo0414](https://clawhub.ai/user/chenmo0414)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill when running command-line tasks on Windows with MSYS2/Git Bash, PowerShell, or WSL. It helps choose the right shell and avoid common silent failures caused by encoding defaults, path conversion, environment persistence, and cross-shell behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags an unpinned external setup command.

Mitigation: Inspect a pinned version of the referenced setup repository before running the one-click setup command, or apply the documented configuration steps manually.

Risk: The skill recommends persistent user-level environment, shell profile, and global Git configuration changes.

Mitigation: Review each persistent change before applying it and limit changes to the specific Windows account or project workflow that needs them.

## Reference(s):

- [windows-shell Skill Page](https://clawhub.ai/chenmo0414/skills/windows-shell)
- [Publisher Profile](https://clawhub.ai/user/chenmo0414)
- [Project Homepage](https://github.com/Chenmo0414/win-encoding-fix)
- [encoding.md](references/encoding.md)
- [gitbash-pitfalls.md](references/gitbash-pitfalls.md)
- [msys2.md](references/msys2.md)
- [shell-routing.md](references/shell-routing.md)
- [wsl.md](references/wsl.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell, PowerShell, Python, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance is organized as a quick routing table with optional reference files for deeper Windows shell, encoding, MSYS2, Git Bash, and WSL details.]

## Skill Version(s):

5.3.0 (source: server release evidence, SKILL.md frontmatter, CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
