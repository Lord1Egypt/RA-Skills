## Description: <br>
Undo gives AI coding agents project file history, snapshots, checkpoints, and restore operations through local Node.js scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[x-guang](https://clawhub.ai/user/x-guang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI coding-agent users use this skill to track file edits, create named checkpoints, list recent change history, and restore a project to a prior snapshot after experimentation or mistaken edits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can copy project contents into persistent local history outside the project. <br>
Mitigation: Avoid running it on projects containing secrets unless exclusions are configured and retention is acceptable. <br>
Risk: The background watcher can retain file changes automatically after it is started. <br>
Mitigation: Start the watcher only deliberately, track its process ID, and stop it when automatic snapshots are no longer needed. <br>
Risk: Undo operations can overwrite files in the working project. <br>
Mitigation: List history and manually review the target checkpoint, timestamp, or step count before running an undo. <br>
Risk: Initialization may attempt to install Git automatically if Git is missing. <br>
Mitigation: Preinstall Git through approved system processes before using the skill. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/x-guang/undo) <br>
- [Undo API Reference](artifact/references/api.md) <br>
- [OpenClaw Skills Documentation](https://openclaws.io/docs/tools/skills/) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [Single-line JSON script results with supporting markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js; the skill's ClawHub metadata declares node as a required binary.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
