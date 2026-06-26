## Description: <br>
Enforces workspace file naming, directory placement, and cleanup rules so agent-created files remain predictable, findable, and traceable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lujun2508](https://clawhub.ai/user/lujun2508) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to keep generated reports, scripts, data, and temporary files inside predictable project directories with consistent names. It is most useful when an agent is creating or organizing local workspace files and the user has not supplied an explicit destination path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can prompt an agent to delete, move, archive, or prune local files based on ambiguous comments about generated outputs. <br>
Mitigation: Require explicit user confirmation before deleting, moving, archiving, or pruning files outside a clearly scoped temporary directory. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/lujun2508/workspace-guardian-by-lujun) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration] <br>
**Output Format:** [Markdown instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Applies to local file organization and cleanup behavior when no explicit output path is provided.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
