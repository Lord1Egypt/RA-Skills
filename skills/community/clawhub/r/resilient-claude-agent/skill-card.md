## Description:

Run Claude Code sessions in tmux for fire-and-forget execution with crash recovery, model routing, and structured task state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mattmartinez](https://clawhub.ai/user/mattmartinez)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding-agent operators use this skill to delegate long-running coding, debugging, refactoring, test, documentation, review, and analysis tasks to an unattended Claude Code session with monitoring and resume behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs unattended Claude Code sessions with permission checks disabled, giving the background agent broad authority in the mounted project environment.

Mitigation: Run it only in a disposable container, VM, or dedicated low-privilege account with only the intended project mounted.

Risk: Background tmux/nohup activity and local logs may retain sensitive task output.

Mitigation: Avoid hosts with exposed SSH keys, cloud credentials, browser profiles, production databases, unrelated repositories, or privileged local services.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mattmartinez/skills/resilient-claude-agent)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and task-state conventions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces instructions for tmux-managed Claude Code execution, monitor configuration, task manifests, logs, and cleanup.]

## Skill Version(s):

1.0.17 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
