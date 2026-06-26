## Description: <br>
Self Improving Agent CN is a local memory skill that records command errors, user corrections, and best practices so an agent can consult them during future work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhengxinjipai](https://clawhub.ai/user/zhengxinjipai) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to persist local records of failed commands, corrections, and best practices, then check those records before repeating similar work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory may store sensitive details, private paths, or incorrect guidance. <br>
Mitigation: Require explicit approval for each memory write and regularly inspect or delete JSONL memory entries that contain secrets, private paths, or bad guidance. <br>
Risk: Automatic updates to AGENTS.md, MEMORY.md, backups, or cross-project sync may spread unwanted instructions. <br>
Mitigation: Require approval before any AGENTS.md or MEMORY.md update, git backup, cross-project sync, sudo command, or global install command. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zhengxinjipai/self-improving-agent-cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell commands and JSONL-backed local memory files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes and reads local memory records under ~/.openclaw/memory/self-improving when its helper scripts are used.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
