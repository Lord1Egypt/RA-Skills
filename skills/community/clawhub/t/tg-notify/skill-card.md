## Description: <br>
Sends Telegram notifications to one or more configured recipients by Telegram user ID. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AgohpAI](https://clawhub.ai/user/AgohpAI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and team members use this skill to send alerts, reminders, and task updates through Telegram to specific people or small recipient lists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send user-provided content externally through Telegram using a local bot token. <br>
Mitigation: Before each send, verify the exact message text and recipient chat IDs, and avoid sending secrets, credentials, personal data, or internal-only material unless sharing over Telegram is intended. <br>
Risk: Broad notification triggers may make it easy to prepare or send a Telegram message in the wrong context. <br>
Mitigation: Confirm user intent, recipient list, and delivery result before treating a notification as complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AgohpAI/tg-notify) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, node, a Telegram bot token in local OpenClaw configuration, and intended Telegram chat IDs.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
