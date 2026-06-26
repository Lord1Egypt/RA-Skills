## Description: <br>
Search and analyze your own session logs using jq, and access 50+ models for image generation, video generation, text-to-speech, speech-to-text, music, chat, web search, document parsing, email, and SMS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GodferyLindsay](https://clawhub.ai/user/GodferyLindsay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to inspect local session logs and to invoke a broad SkillBoss API wrapper for model, search, scraping, document, email, and SMS tasks. It is most appropriate when the user intentionally wants third-party API-backed commands under a SkillBoss API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is framed as session-log analysis but mainly provides a broad third-party API wrapper. <br>
Mitigation: Confirm that the intended use is remote SkillBoss API access before installing or using the skill. <br>
Risk: Session logs, tokens, private documents, audio, images, phone numbers, or email content could be sent to external services. <br>
Mitigation: Redact sensitive data and require explicit user approval before each outbound processing or messaging action. <br>
Risk: Email and SMS examples can trigger communication with external recipients. <br>
Mitigation: Use test recipients first and require human confirmation of recipient, content, and purpose before sending. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/GodferyLindsay/session-logss) <br>
- [SkillBoss](https://www.skillboss.co) <br>
- [HeyBoss API Base URL](https://api.heybossai.com/v1) <br>
- [Chat Models](artifact/chat-models.md) <br>
- [Image Models](artifact/image-models.md) <br>
- [Audio Models](artifact/audio-models.md) <br>
- [Search and Scraping Models](artifact/search-models.md) <br>
- [Tool Models](artifact/tools-models.md) <br>
- [Video Models](artifact/video-models.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with curl and bash command examples, model reference tables, and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and may direct the agent to send data or actions to third-party API endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
