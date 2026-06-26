## Description: <br>
AI business coach for Uzbek startups offering tailored advice on idea validation, product development, sales, China sourcing, fundraising, and CIS expansion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevensabiro](https://clawhub.ai/user/stevensabiro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Entrepreneurs and startup operators use this skill in Telegram to get practical coaching for Uzbekistan and CIS-focused startup work, including validation, MVP planning, sales, sourcing, expansion, fundraising preparation, and consent-based check-ins. <br>

### Deployment Geography for Use: <br>
Global, with guidance focused on Uzbekistan and CIS markets. <br>

## Known Risks and Mitigations: <br>
Risk: Telegram bot credentials could be exposed or overused if shared across unrelated deployments. <br>
Mitigation: Use a dedicated Telegram bot token for this skill and rotate it if access is no longer needed. <br>
Risk: Uploaded pitch decks or business plans may contain confidential business information. <br>
Mitigation: Avoid uploading sensitive documents unless necessary and review what is shared before file-reading workflows. <br>
Risk: The skill stores personal startup context locally for continuity. <br>
Mitigation: Use the documented `/mydata` and `/deletedata` commands to review or remove stored local context. <br>
Risk: Broad trigger words such as "coach" or "mentor" may activate the skill unintentionally. <br>
Mitigation: Confirm intent before relying on startup-coaching output, especially in mixed-purpose Telegram conversations. <br>
Risk: Scheduled follow-up messages can contact users proactively. <br>
Mitigation: Enable reminders only after explicit opt-in and confirm consent before the first scheduled check-in. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stevensabiro/uzstartup-coach) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, markdown] <br>
**Output Format:** [Concise Telegram-ready coaching responses with short paragraphs, bullets, commands, and optional follow-up prompts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use uploaded files, web search results, locally stored user context, and consent-gated scheduled reminders when available.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
