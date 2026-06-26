## Description: <br>
Autonomous internet exploration skill. Your agent roams the web driven by its own curiosity, discovers interesting things, and sends illustrated "postcards" — personal letters with AI-generated art — to a chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangwenyu2](https://clawhub.ai/user/yangwenyu2) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent operators use this skill to let an OpenClaw agent periodically explore public web content, write personal postcard-style updates, generate an illustration, and send the result to a configured chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can keep rescheduling autonomous trips, post to chat, and spend API credits. <br>
Mitigation: Use bounded intervals, monitor API usage and chat output, and keep the openclaw cron and watchdog stop commands available before enabling recurring operation. <br>
Risk: The skill stores and sources local travel configuration and runtime memory indefinitely. <br>
Mitigation: Inspect the generated .travel-config, review file permissions, and remove runtime configuration or journal files when the travel loop is no longer needed. <br>
Risk: The skill browses public web pages and sends image prompts to OpenRouter through the configured model provider. <br>
Mitigation: Run it only when public-web browsing and external model-provider calls are intended, and review generated postcards for unwanted content before relying on them. <br>


## Reference(s): <br>
- [Travel Lobster on ClawHub](https://clawhub.ai/yangwenyu2/travel-lobster) <br>
- [Travel prompt reference](references/travel-prompt.md) <br>
- [OpenRouter chat completions API](https://openrouter.ai/api/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Images, Shell commands, Configuration] <br>
**Output Format:** [Postcard-style Markdown text with an AI-generated image, source link, local journal updates, and scheduling commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OpenClaw, bash, python3, envsubst, and OPENROUTER_API_KEY; default operation can reschedule future trips until stopped.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
