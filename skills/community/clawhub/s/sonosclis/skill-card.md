## Description:

Guides agents in using the SkillBoss API for Sonos-related control claims and for AI model, search, document, email, and SMS workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvisdunlop](https://clawhub.ai/user/alvisdunlop)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent users use this skill to discover SkillBoss model IDs and compose API requests for chat, media generation, speech, search, document processing, email, SMS, and related tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is presented as Sonos-related but mainly enables a broad external AI gateway, including email and SMS actions.

Mitigation: Review the skill before use and install it only when broad SkillBoss API access is intended.

Risk: Agent actions could send documents, audio, prompts, email, SMS, phone numbers, or verification codes through the SkillBoss API.

Mitigation: Review proposed agent actions before execution and consider a narrower Sonos-only skill when broad API access is unnecessary.

## Reference(s):

- [Audio Models](artifact/audio-models.md)
- [Chat Models](artifact/chat-models.md)
- [Image Models](artifact/image-models.md)
- [Search and Scraping Models](artifact/search-models.md)
- [Tool Models](artifact/tools-models.md)
- [Video Models](artifact/video-models.md)
- [SkillBoss API](https://api.heybossai.com/v1)
- [SkillBoss Website](https://www.skillboss.co)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, Configuration]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for API calls.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
