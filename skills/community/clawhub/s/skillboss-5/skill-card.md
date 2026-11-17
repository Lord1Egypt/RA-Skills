## Description:

Swiss-knife for AI agents: 50+ models for image generation, video generation, text-to-speech, speech-to-text, music, chat, web search, document parsing, email, and SMS, with smart routing for cost saving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marjoriebroad](https://clawhub.ai/user/marjoriebroad)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to discover and call SkillBoss models across chat, image, video, audio, search, document processing, email, and SMS workflows through curl-based API examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, files or file URLs, audio, images, document content, search queries, email details, phone numbers, and API-key-linked metadata may be sent to SkillBoss and downstream providers.

Mitigation: Use only data you are authorized to share, avoid regulated or confidential data unless approved, and review provider handling requirements before live use.

Risk: Email and SMS workflows can send messages to external recipients.

Mitigation: Require explicit user confirmation before sending email or SMS messages.

Risk: Live API calls require a SkillBoss API key.

Mitigation: Store SKILLBOSS_API_KEY as a secret and avoid exposing it in prompts, logs, shared terminals, or generated artifacts.

## Reference(s):

- [ClawHub Skillboss release page](https://clawhub.ai/marjoriebroad/skills/skillboss-5)
- [marjoriebroad ClawHub profile](https://clawhub.ai/user/marjoriebroad)
- [SkillBoss website](https://www.skillboss.co)
- [SkillBoss API base URL](https://api.heybossai.com/v1)
- [Audio Models](artifact/audio-models.md)
- [Chat Models](artifact/chat-models.md)
- [Image Models](artifact/image-models.md)
- [Search & Scraping Models](artifact/search-models.md)
- [Tool Models](artifact/tools-models.md)
- [Video Models](artifact/video-models.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for live API calls.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
