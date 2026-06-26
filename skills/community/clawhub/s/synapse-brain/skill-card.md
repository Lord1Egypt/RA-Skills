## Description: <br>
Synapse Brain is an OpenClaw persistent orchestration agent for cross-session task management, subagent dispatch, state persistence, and knowledge-skill interoperability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ankechenlab-node](https://clawhub.ai/user/ankechenlab-node) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to resume long-running project sessions, route user requests to code or knowledge skills, dispatch subagents, and preserve task history across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores project names, task titles, notes, failures, and history in local state files. <br>
Mitigation: Do not put secrets or sensitive data in project names, task titles, notes, or failure messages; review local state before sharing logs or backups. <br>
Risk: The installer can overwrite or remove an existing ~/.openclaw/skills/synapse-brain installation. <br>
Mitigation: Back up the existing installation before running install.sh and review the installer behavior with --dry-run first. <br>
Risk: State-file paths depend on user-supplied project names. <br>
Mitigation: Use simple project names without slashes or .. and request maintainer-side path validation before relying on it for important history. <br>
Risk: Archive behavior may affect retained task history. <br>
Mitigation: Back up ~/.openclaw/brain-state and confirm archive retention behavior before depending on it for important project records. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ankechenlab-node/synapse-brain) <br>
- [Synapse Brain Homepage](https://github.com/ankechenlab-node/synapse-brain) <br>
- [Architecture Reference](references/architecture.md) <br>
- [synapse-code](https://github.com/ankechenlab-node/synapse-code) <br>
- [synapse-wiki](https://github.com/ankechenlab-node/synapse-wiki) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and command-oriented text with JSON state/configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains local project state under ~/.openclaw/brain-state when installed and used.] <br>

## Skill Version(s): <br>
2.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
