## Description:

Helps agents configure, debug, and optimize Visual Studio Code settings, launch and task files, extensions, keybindings, formatting, remote development, workspaces, and editor performance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to diagnose VS Code behavior and produce editor configuration or guidance for settings scopes, formatting, debugging, tasks, extensions, remotes, workspaces, and forks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically keeps shared local records about VS Code setup, repositories, extensions, remote hosts, and access-pointer locations.

Mitigation: Install only if this local knowledge base is acceptable; review or disable automatic memory behavior for sensitive work and periodically inspect and prune the declared Clawic data paths.

Risk: Editor settings, task definitions, terminal environments, and dev container files may contain credentials or secret-bearing values.

Mitigation: Store only secret pointers, strip credential values from saved notes, and review generated or persisted configuration before reuse.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/vscode)
- [Clawic VSCode Skill Page](https://clawic.com/skills/vscode)
- [VSCode Skill Definition](artifact/SKILL.md)
- [Security Guidance](artifact/security.md)
- [Memory Template](artifact/memory-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with JSON snippets, shell commands, and configuration blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May maintain local VS Code memory and configuration notes under the declared Clawic paths when durable setup facts are produced.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
