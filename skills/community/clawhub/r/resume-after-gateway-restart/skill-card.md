## Description:

Helps agents schedule a durable OpenClaw restart-and-resume workflow before restarting the OpenClaw gateway, then return to the original chat and continue work after restart.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bobbylindsey](https://clawhub.ai/user/bobbylindsey)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill when an OpenClaw gateway restart is needed during an active task and the agent should resume automatically in the original chat. It guides the agent to save resume context, schedule follow-up cron turns, and restart the gateway after the pre-restart message has time to deliver.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A wrong session key or delivery route could send the post-restart response to the wrong chat.

Mitigation: Verify the session key, delivery channel, and delivery target before scheduling the cron jobs.

Risk: An inaccurate resume note could cause the follow-up agent turn to continue the wrong task.

Mitigation: Review memory/post-restart-task.md before restart and make the next step explicit and narrow.

Risk: Restarting the gateway interrupts active agent work.

Mitigation: Send a standalone pre-restart notice, schedule the restart with a short delay, and confirm the cron jobs exist before restart.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bobbylindsey/skills/resume-after-gateway-restart)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and file snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a resume-note template, cron scheduling commands, and delayed restart command guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
