## Description:

Stream long-running task progress into the OpenClaw chat UI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liyooyin](https://clawhub.ai/user/liyooyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to monitor long-running model training, evaluation, inference, preprocessing, benchmark, and shell jobs from within an OpenClaw chat session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Command output or tailed log contents may include secrets, personal data, proprietary information, or attacker-controlled text that is injected into the OpenClaw chat session.

Mitigation: Use the skill only with logs and commands whose output is appropriate for the selected chat session; avoid sensitive or untrusted logs and prefer low-privilege sessions for automated updates.

Risk: The run mode executes a user-provided shell command while streaming its output.

Mitigation: Review the command and working directory before starting run mode, and run it with the least privilege needed for the task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liyooyin/skills/task-progress-stream)
- [ClawHub publisher profile](https://clawhub.ai/user/liyooyin)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown progress summaries with optional status JSON, status Markdown, and stream log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Progress summaries can include state, percent complete, epoch, step, loss, learning rate, validation metric, best metric, ETA, speed, and recent log lines.]

## Skill Version(s):

0.1.0 (source: server release metadata, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
