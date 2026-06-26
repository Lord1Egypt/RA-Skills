## Description: <br>
Creates one-shot reminders from Spanish natural-language time expressions, defaults scheduling to America/Bogota, logs reminders in markdown, and emits cron job JSON for OpenClaw cron. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[StarAtheris](https://clawhub.ai/user/StarAtheris) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw agents use this skill to convert Spanish reminder requests into scheduled one-shot cron jobs and a local reminder log. It is intended for users who want reminders interpreted in the America/Bogota timezone. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review says the skill can send reminder text to a hardcoded Telegram chat even though documentation says it does not use external APIs or outside IDs. <br>
Mitigation: Review before installing, set ARYA_TELEGRAM_CHAT_ID to the intended chat, and avoid sensitive reminder text unless local storage and Telegram delivery are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/StarAtheris/staratheris-arya-reminders) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [JSON cron job request with markdown reminder log guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash and python3; reminder delivery uses the cron tool and Telegram channel configuration.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
