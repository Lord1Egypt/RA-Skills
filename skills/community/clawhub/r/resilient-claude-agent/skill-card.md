## Description: <br>
Run Claude Code sessions in tmux for fire-and-forget execution with crash recovery, model routing, and structured task state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mattmartinez](https://clawhub.ai/user/mattmartinez) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding orchestrators use this skill to delegate long-running coding tasks to Claude Code in tmux while preserving task state and recovering from crashes or hangs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Claude Code runs unattended with permission prompts disabled and can read, write, and execute commands in the selected project. <br>
Mitigation: Install only in trusted workspaces under a trusted orchestrator, and prefer a dedicated user, VM, or container for execution. <br>
Risk: A compromised or unexpected claude or openclaw binary on PATH changes the behavior of delegated tasks and notifications. <br>
Mitigation: Audit the claude and openclaw binaries on PATH before use. <br>
Risk: Cleanup can affect tmux sessions using the claude- prefix. <br>
Mitigation: Avoid unrelated tmux sessions with names that use the claude- prefix. <br>
Risk: Captured task output and temp logs may contain secrets from agent activity. <br>
Mitigation: Restrict log permissions and clean up temporary directories after reviewing results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mattmartinez/resilient-claude-agent) <br>
- [Publisher profile](https://clawhub.ai/user/mattmartinez) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with shell command blocks and task-state file conventions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires tmux, claude, and openclaw binaries; task output may include manifests, logs, exit codes, and completion markers.] <br>

## Skill Version(s): <br>
1.0.17 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
