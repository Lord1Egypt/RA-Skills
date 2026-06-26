## Description: <br>
Troubleshooting guide for vx issues. Use when encountering installation failures, version conflicts, PATH issues, or other vx problems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loonghao](https://clawhub.ai/user/loonghao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to diagnose and recover from vx installation failures, version conflicts, PATH issues, runtime errors, configuration problems, CI failures, and corrupted local state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote installer commands can execute unreviewed code when copied directly from troubleshooting output. <br>
Mitigation: Require explicit user approval before running installer commands, and prefer reviewed, pinned installation steps. <br>
Risk: Reset and lock-file recovery steps can delete local vx state or project lock data. <br>
Mitigation: Confirm backups, scope, and consequences before deleting ~/.vx or vx.lock. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/loonghao/vx-troubleshooting) <br>
- [vx Documentation](https://github.com/loonghao/vx#readme) <br>
- [vx GitHub Issues](https://github.com/loonghao/vx/issues) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and troubleshooting decision steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local repair commands, remote installer commands, and destructive reset steps that require user review before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
