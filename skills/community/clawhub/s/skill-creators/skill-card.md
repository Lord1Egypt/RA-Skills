## Description:

Guide for creating effective skills for Clawdbot agents with access patterns for 50+ models spanning chat, image, video, audio, search, document processing, email, and SMS through the SkillBoss API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to discover SkillBoss model options and draft calls or configuration for chat, media generation, search, document processing, email, SMS, and smart model routing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided prompts, documents, audio, images, or contact data may be sent to SkillBoss and downstream providers.

Mitigation: Do not use the skill with secrets, private documents, sensitive audio, or contact data unless the service and downstream data handling are trusted.

Risk: Email and SMS actions can contact third parties or trigger verification workflows.

Mitigation: Require explicit user confirmation and review recipients, phone numbers, message body, and purpose before sending email or SMS.

Risk: The manifest name and broad API surface may make the skill's actual scope unclear during installation or use.

Mitigation: Review the skill before installation and confirm the requested model, action, and SKILLBOSS_API_KEY requirement before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tobeyrebecca/skills/skill-creators)
- [Publisher Profile](https://clawhub.ai/user/tobeyrebecca)
- [SkillBoss Website](https://www.skillboss.co)
- [SkillBoss API Base URL](https://api.heybossai.com/v1)
- [Audio Models](artifact/audio-models.md)
- [Chat Models](artifact/chat-models.md)
- [Image Models](artifact/image-models.md)
- [Search and Scraping Models](artifact/search-models.md)
- [Tool Models](artifact/tools-models.md)
- [Video Models](artifact/video-models.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY; generated API responses may include text, URLs, media outputs, extracted document content, or message delivery status.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
