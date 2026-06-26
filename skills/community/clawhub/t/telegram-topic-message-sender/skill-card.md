## Description: <br>
Wrap sending a Telegram message to a fixed topic into one script call. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shing19](https://clawhub.ai/user/shing19) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to send plain-text notifications or status messages to a specific Telegram supergroup topic through an OpenClaw-configured channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent using this skill can post messages to the configured Telegram group topic. <br>
Mitigation: Confirm the OpenClaw channel auth and any TG_DEFAULT_CHANNEL, TG_DEFAULT_CHAT_ID, and TG_DEFAULT_TOPIC_ID values point only to the intended group and topic before installing or running it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shing19/telegram-topic-message-sender) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Sends plain-text messages only; markdown and HTML parse modes are intentionally not enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
