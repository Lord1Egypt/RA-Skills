## Description: <br>
Executes commands on remote hosts over SSH using aliases, SSH config, tmux sessions, and private keys, with guardrails for host validation and destructive commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rickkbarbosa](https://clawhub.ai/user/rickkbarbosa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect remote Linux or server state, run one-off SSH commands, reuse configured SSH aliases, and drive tmux-based remote workflows. It is best suited for user-directed, key-based remote diagnostics and operational tasks where the exact host and command can be reviewed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run remote commands over SSH and may affect systems with the privileges of the selected SSH account. <br>
Mitigation: Confirm the exact host and full command before use, prefer least-privilege SSH aliases or keys, and avoid root or production credentials unless the task requires them. <br>
Risk: State-changing or destructive commands could alter files, services, packages, containers, networks, or data on a remote host. <br>
Mitigation: Start with read-only inspection, require explicit approval for mutating commands, and use the destructive-command confirmation guard only after the user has reviewed the complete command. <br>
Risk: SSH credentials and key paths are sensitive operational details. <br>
Mitigation: Use key-based authentication without pasting private keys or passwords into chat, and avoid exposing private-key contents or credential metadata in logs or responses. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/rickkbarbosa/ssh-executor) <br>
- [Publisher profile](https://clawhub.ai/user/rickkbarbosa) <br>
- [SSH Executor Safety Notes](references/safety.md) <br>
- [Clawdis metadata](metadata:openclaw/os=linux,darwin;requires=ssh,bash,python3) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured SSH execution results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May report SSH success, exit code, stdout, stderr, resolved host metadata, and recommended next safe steps.] <br>

## Skill Version(s): <br>
1.1.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
