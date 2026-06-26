## Description: <br>
Memory Manager helps OpenClaw agents manage local memory sharing, archiving, cleanup, and operation logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wcwudi](https://clawhub.ai/user/wcwudi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to maintain local memory directories, share selected memory between main and sub-agents, archive files, and review operation logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured paths or agent mappings may point to the wrong local workspace. <br>
Mitigation: Verify config/default.json paths and agent access before running commands. <br>
Risk: Archive and cleanup examples can move or delete memory files if run carelessly. <br>
Mitigation: Run archive and cleanup commands in test or preview mode first, keep backups, and require explicit confirmation for destructive actions. <br>
Risk: Shared memory or logs may expose sensitive content to another agent or local user. <br>
Mitigation: Do not place secrets or private data in shared memory, archives, or logs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wcwudi/wcwudi-memory-manager) <br>
- [README](artifact/README.md) <br>
- [Quick Start Guide](artifact/docs/QUICK_START.md) <br>
- [Architecture Guide](artifact/docs/ARCHITECTURE.md) <br>
- [Default Configuration](artifact/config/default.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with PowerShell command examples and JSON configuration references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe local file paths, archive actions, and operation-log checks; users should confirm before running file-moving commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, artifact config/default.json, and artifact SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
