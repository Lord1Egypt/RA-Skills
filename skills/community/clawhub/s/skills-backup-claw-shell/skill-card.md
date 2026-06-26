## Description: <br>
Executes shell commands inside a dedicated tmux session named claw and returns captured pane output to the agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Gexsta](https://clawhub.ai/user/Gexsta) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill when an agent needs to run shell commands in a persistent tmux session and inspect the resulting terminal output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives the agent broad terminal access through tmux. <br>
Mitigation: Install only when terminal-like access is intended, review commands carefully before execution, and avoid using it in environments with sensitive data. <br>
Risk: Weak safety checks may miss harmful commands or command variants. <br>
Mitigation: Require explicit human approval for destructive, privileged, or system-level commands and prefer argument-safe execution controls. <br>
Risk: Persistent tmux sessions may retain sensitive terminal output. <br>
Mitigation: Avoid leaving secrets in the tmux session and clear or isolate session output when sensitive commands are involved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Gexsta/skills-backup-claw-shell) <br>
- [Publisher profile](https://clawhub.ai/user/Gexsta) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [JSON object containing the submitted command and captured terminal output, or an error object] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs commands in a tmux session named claw and captures recent pane output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
