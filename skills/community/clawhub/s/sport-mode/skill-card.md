## Description:

Activate "Sport Mode" for high-frequency monitoring (default 3m heartbeat) and auto-cleanup. Use when supervising intense tasks (Codex, builds, migrations).

This skill is ready for commercial/non-commercial use.

## Publisher:

[l1vein](https://clawhub.ai/user/l1vein)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use Sport Mode to temporarily increase OpenClaw heartbeat frequency for monitoring long-running builds, coding-agent work, deployments, or turn-based workflows, then return heartbeat behavior to the default interval when complete.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently increase heartbeat frequency and repeatedly execute instructions from HEARTBEAT.md without a built-in stop limit.

Mitigation: Use explicit, narrow tasks with a termination condition, and include a command or instruction to run sport-mode off when the task completes.

Risk: Activating the skill overwrites HEARTBEAT.md, which can discard existing heartbeat instructions.

Mitigation: Back up or review any existing HEARTBEAT.md content before enabling Sport Mode.

Risk: Broad autonomous tasks can authorize actions such as commits or deployments if the user writes them into the heartbeat task.

Mitigation: Avoid tasks that authorize commits, deployments, or other high-impact actions unless that autonomy is intended and bounded.

## Reference(s):

- [ClawHub Sport Mode skill page](https://clawhub.ai/l1vein/skills/sport-mode)
- [Artifact README](artifact/README.md)
- [Artifact Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Markdown, Guidance]

**Output Format:** [Markdown guidance with shell command examples and HEARTBEAT.md task content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update OpenClaw heartbeat configuration and write or clear HEARTBEAT.md during use.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
