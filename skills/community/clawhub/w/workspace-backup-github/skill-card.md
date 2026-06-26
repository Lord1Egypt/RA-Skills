## Description: <br>
Backs up AI agent workspace files to a private GitHub repository through guided setup, manual runs, and scheduled backups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ziqi-jin](https://clawhub.ai/user/ziqi-jin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agent users use this skill to preserve OpenClaw, Claude Code, Cursor, and similar workspaces by committing selected workspace files to a private GitHub repository and scheduling repeat backups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow asks for a GitHub token and the shell script can place that token in a git remote URL. <br>
Mitigation: Do not paste tokens into chat or store them in remote URLs; prefer GitHub CLI, a credential helper, or a narrowly scoped token stored outside conversation history. <br>
Risk: Backups may upload sensitive workspace files to GitHub. <br>
Mitigation: Use a private repository and review the exact backup set for secrets before the first push and after backup-scope changes. <br>
Risk: Restore commands may overwrite local workspace state. <br>
Mitigation: Keep a current local copy and review restored files before replacing active workspace content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ziqi-jin/workspace-backup-github) <br>
- [Publisher profile](https://clawhub.ai/user/ziqi-jin) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with setup prompts and inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides GitHub repository, token, backup schedule, status, and restore workflows.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence, created 2026-03-16) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
