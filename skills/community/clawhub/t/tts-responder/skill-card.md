## Description: <br>
Convierte respuestas de texto a audio OGG con Piper y las envía por Telegram cuando se activa el modo de voz. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jgf78](https://clawhub.ai/user/jgf78) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Telegram bot operators use this skill to turn assistant text into spoken OGG voice replies and send them to a configured Telegram chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated voice replies and caption text can be shared with Telegram for the configured chat. <br>
Mitigation: Use spoken mode only when Telegram sharing is acceptable for the conversation content. <br>
Risk: A misconfigured bot token or chat ID could send audio to the wrong Telegram destination. <br>
Mitigation: Use a limited bot token and verify CHAT_ID before enabling voice replies. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jgf78/tts-responder) <br>
- [Skill homepage](https://github.com/openclaw/skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and environment variable configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces or sends OGG Opus audio through the bundled shell script when configured with Telegram credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
