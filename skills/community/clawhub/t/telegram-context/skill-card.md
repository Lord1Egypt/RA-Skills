## Description: <br>
Toggle-enabled skill that fetches Telegram message history at session start for conversational continuity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fourthdensity](https://clawhub.ai/user/fourthdensity) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to preserve conversational continuity in Telegram chats by fetching recent messages into the agent context at session start or on demand. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recent messages from the current Telegram chat are read into the agent context and sent to the configured model provider. <br>
Mitigation: Use manual fetch or a low fetch count for sensitive chats, and turn the skill off when continuity is not needed. <br>
Risk: Fetched messages may include sensitive conversation history or appear in session logs depending on logging configuration. <br>
Mitigation: Avoid auto-fetch for sensitive conversations and disable the skill before discussing sensitive topics. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fourthdensity/telegram-context) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples and configuration state] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can fetch recent messages from the current Telegram chat into the agent context when enabled or manually requested.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
