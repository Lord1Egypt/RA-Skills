## Description: <br>
Token Stats Pkg lets users choose Hermes, Claude Code, CodeX, or OpenClaw and view local token usage statistics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhouhaoyong](https://clawhub.ai/user/zhouhaoyong) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and AI-assistant users use this skill to inspect token usage, compare activity across time ranges, monitor active sessions, and export local usage data for supported assistants on the machine where it is installed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The utility reads local assistant usage and history files for Hermes, Claude Code, CodeX, and OpenClaw. <br>
Mitigation: Install and run it only in environments where reading those local assistant data files is acceptable. <br>
Risk: The setup command can create a global token-stats wrapper in ~/.local/bin. <br>
Mitigation: Run setup only when a global command is desired, and remove ~/.local/bin/token-stats if the shortcut is no longer wanted. <br>
Risk: Export mode can write local JSON or CSV usage reports to a selected directory. <br>
Mitigation: Export only to trusted locations and review exported usage reports before sharing them. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/zhouhaoyong/token-stats-pkg) <br>
- [README.md](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text and Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can display interactive menus, live monitoring output, comparison tables, and optional JSON or CSV exports.] <br>

## Skill Version(s): <br>
2.0.9 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
