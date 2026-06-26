## Description: <br>
Reliably resumes agent work after an OpenClaw gateway restart by saving restart context, scheduling one-shot cron resume jobs, and returning the reply to the original chat route. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bobbylindsey](https://clawhub.ai/user/bobbylindsey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when an OpenClaw gateway restart would otherwise interrupt an active task. It helps preserve context, schedule a post-restart wakeup, and deliver the follow-up response back to Discord or Telegram. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates local OpenClaw cron jobs that send messages after a gateway restart. <br>
Mitigation: Review the generated cron job names, route, model, and message timing before restart, and remove stale jobs when resume automation is no longer needed. <br>
Risk: The skill restarts the user-level OpenClaw gateway service through a delayed systemd unit. <br>
Mitigation: Use only when a gateway restart is intended, schedule the restart after notifying the user, and confirm the resume cron jobs exist before the service is restarted. <br>
Risk: The resume workflow writes local restart status to memory/post-restart-task.md. <br>
Mitigation: Keep the file limited to task state needed for restart recovery and avoid storing sensitive information in the resume context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bobbylindsey/resume-after-gateway-restart) <br>
- [Publisher profile](https://clawhub.ai/user/bobbylindsey) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell command examples and status-file guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local cron scheduling commands, a restart command, and guidance for updating memory/post-restart-task.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
