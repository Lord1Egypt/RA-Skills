## Description: <br>
Automatically enforces workspace file size limits, archives stale or bloated files, and organizes root contents to maintain efficient AI agent context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[casperzinou](https://clawhub.ai/user/casperzinou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agent operators use this skill to keep long-running agent workspaces lean by trimming boot files, archiving stale notes, and moving misplaced root files into archive locations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The cleanup workflow can automatically change, move, trim, or delete important workspace files without an interactive review step. <br>
Mitigation: Review the target workspace path and back up AGENTS.md, MEMORY.md, STATE.md, USER.md, and memory notes before enabling scheduled or unattended runs. <br>
Risk: The bundled script uses a hardcoded /root/.openclaw/workspace path and may affect the wrong workspace if reused unchanged. <br>
Mitigation: Update the workspace path for the intended environment and test manually before installing cron automation. <br>
Risk: Automatic deletion of very small memory files and trimming of boot files can remove useful context. <br>
Mitigation: Prefer archive-only behavior or a dry-run review step for critical workspaces, and inspect archive output after initial runs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/casperzinou/talonforge-workspace-hygiene) <br>
- [Skill Instructions](artifact/SKILL.md) <br>
- [Workspace Hygiene Script](artifact/workspace-hygiene.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell command and cron examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May append a workspace hygiene report to the current daily note when the bundled shell script is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
