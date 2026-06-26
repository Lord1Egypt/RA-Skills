## Description: <br>
Guides Clawdbot agents in creating effective skills and using the SkillBoss API for chat, image, video, audio, music, search, document processing, email, and SMS workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TobeyRebecca](https://clawhub.ai/user/TobeyRebecca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to configure Clawdbot agents with SkillBoss API access for model discovery, model invocation, smart routing, and multimodal automation tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives agents broad external API, email, SMS, document, audio, media, scraping, and smart-routing capabilities. <br>
Mitigation: Require explicit approval before email, SMS, batch messaging, OTP, document parsing, audio transcription, scraping, or smart-routing calls. <br>
Risk: Requests may send prompts, documents, audio, or other user data to SkillBoss and downstream providers. <br>
Mitigation: Avoid confidential or regulated data unless the deployment accepts SkillBoss and downstream provider handling. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/TobeyRebecca/skill-creators) <br>
- [SkillBoss website](https://www.skillboss.co) <br>
- [SkillBoss API base](https://api.heybossai.com/v1) <br>
- [Chat Models](artifact/chat-models.md) <br>
- [Image Models](artifact/image-models.md) <br>
- [Video Models](artifact/video-models.md) <br>
- [Audio Models](artifact/audio-models.md) <br>
- [Search & Scraping Models](artifact/search-models.md) <br>
- [Tool Models](artifact/tools-models.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for examples that call SkillBoss APIs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
