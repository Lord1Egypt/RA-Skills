## Description: <br>
Task Interrupt Pro helps an agent stop a targeted local subtask process by creating a stop flag and escalating from SIGINT to SIGTERM or SIGKILL after validating the session and PID. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tsangho](https://clawhub.ai/user/tsangho) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when a local OpenClaw-style agent task is stuck or unresponsive and they need to stop a specific session without issuing the platform /stop command. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can terminate local subprocesses, including escalation to SIGKILL when gentler signals do not stop the target. <br>
Mitigation: Install only when intentional process interruption is needed, verify the target SESSION_ID before use, and avoid broad natural-language auto-triggers. <br>
Risk: Forced termination can interrupt work in progress and may corrupt outputs from a stuck task. <br>
Mitigation: Use the stop-flag and SIGINT path first, and avoid this skill for tasks where abrupt termination could damage important state. <br>
Risk: The skill stores PID, stop-flag, lock, and audit files in shared /tmp paths. <br>
Mitigation: Review local file permissions and consider moving state files to a private runtime directory before relying on it in shared environments. <br>


## Reference(s): <br>
- [Task Interrupt Pro on ClawHub](https://clawhub.ai/tsangho/task-interrupt-pro) <br>
- [tsangho publisher profile](https://clawhub.ai/user/tsangho) <br>
- [OpenClaw Skills documentation](https://docs.openclaw.ai/tools/skills) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance, configuration] <br>
**Output Format:** [Markdown guidance with bash command examples and local shell script invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash on Linux or macOS; uses local PID, stop-flag, lock, and audit files under /tmp.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
