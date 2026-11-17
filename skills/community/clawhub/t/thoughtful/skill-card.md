## Description: <br>
Your thoughtful companion for WhatsApp - remembers what matters, helps you stay present in your relationships. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[regalstreak](https://clawhub.ai/user/regalstreak) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to turn selected WhatsApp direct messages and whitelisted group chats into relationship-aware summaries, pending-task reminders, and communication coaching. It helps users notice commitments, tone shifts, quiet conversations, and suggested follow-ups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private WhatsApp-derived content is processed by an LLM workflow and may be delivered to a Telegram destination. <br>
Mitigation: Confirm the destination topic before enabling delivery, limit tracked chats to direct messages and groups you intend to summarize, and avoid enabling the skill unless this data flow is acceptable. <br>
Risk: The skill stores local JSON state, message context, summaries, and prompt files that may contain sensitive relationship or conversation details. <br>
Mitigation: Review where the data directory is stored, set an appropriate retention policy, and delete or minimize raw message context after each run when possible. <br>
Risk: Scheduled sync and summary jobs can repeatedly process new private messages without manual review. <br>
Mitigation: Verify the cron schedule, understand how to disable the jobs, and test a manual run before enabling recurring automation. <br>


## Reference(s): <br>
- [Thoughtful ClawHub listing](https://clawhub.ai/regalstreak/thoughtful) <br>
- [Publisher profile](https://clawhub.ai/user/regalstreak) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries, shell commands, JSON configuration, and natural-language guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads WhatsApp message and chat data via wacli-readonly, writes local JSON state and prompt files, and prepares summaries for LLM-assisted delivery.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
