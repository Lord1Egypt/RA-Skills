## Description:

Swiss-knife for AI agents with 50+ models for image generation, video generation, text-to-speech, speech-to-text, music, chat, web search, document parsing, email, and SMS, with smart routing for cost saving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yshuolu](https://clawhub.ai/user/yshuolu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Skillboss to call third-party AI and utility APIs through a single SkillBoss API key for chat, media generation, search, document processing, messaging, and smart model routing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses SkillBoss as a third-party cloud gateway for prompts, files, audio, images, documents, and generated content.

Mitigation: Avoid sending secrets, regulated data, private documents, or personal data unless the user has authorization and the deployment policy permits it.

Risk: The skill includes live email, SMS, and batch notification capabilities.

Mitigation: Require explicit confirmation before any email, SMS, OTP, or batch notification action, and verify recipients, content, and authorization before sending.

## Reference(s):

- [ClawHub Skillboss release page](https://clawhub.ai/yshuolu/skills/skillboss-swissknife)
- [SkillBoss API base URL](https://api.heybossai.com/v1)
- [SkillBoss website](https://www.skillboss.co)
- [Chat model reference](artifact/chat-models.md)
- [Image model reference](artifact/image-models.md)
- [Video model reference](artifact/video-models.md)
- [Audio model reference](artifact/audio-models.md)
- [Search and scraping model reference](artifact/search-models.md)
- [Tool model reference](artifact/tools-models.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with cURL command examples and JSON API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and may return model-specific text, URLs, generated media, parsed documents, email/SMS action results, or search results.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
