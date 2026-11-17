## Description:

Task Interrupt Pro helps an agent stop stuck subtask processes by creating stop flags and escalating from interrupt signals to forced termination when needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tsangho](https://clawhub.ai/user/tsangho)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to give an agent a message-triggered way to stop unresponsive subtasks while avoiding system-level abort commands. It is intended for controlled Linux or macOS environments where task processes are expected to cooperate with the provided stop-flag and PID-file pattern.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad stop triggers can cause unintended task termination.

Mitigation: Require explicit user confirmation or narrower command matching before sending termination signals.

Risk: Shared temporary PID and flag files can be unsafe on shared or privileged hosts.

Mitigation: Run the skill as an ordinary user and avoid shared or privileged hosts until temporary-file handling is reviewed and hardened.

Risk: Forced termination can lose unsaved work or leave partial state.

Mitigation: Prefer cooperative stop flags and interrupt signals first, and reserve forced termination for unresponsive tasks.

## Reference(s):

- [Task Interrupt Pro on ClawHub](https://clawhub.ai/tsangho/skills/task-interrupt-pro)
- [OpenClaw Skills documentation](https://docs.openclaw.ai/tools/skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May issue process-termination commands and status confirmations for targeted task sessions.]

## Skill Version(s):

1.0.4 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
