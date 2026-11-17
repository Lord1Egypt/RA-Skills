## Description:

Pub Youtube gives agents YouTube transcript retrieval guidance and broad SkillBoss API examples for chat, media generation, speech, search, document processing, email, and SMS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abeltennyson](https://clawhub.ai/user/abeltennyson)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to fetch YouTube transcript content and call SkillBoss models for chat, media, search, scraping, document parsing, email, and SMS tasks. Review it as a broad third-party API gateway, not only as a YouTube transcript helper.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package is labeled as a YouTube transcript helper but documents broad SkillBoss API capabilities including model calls, search, scraping, email, SMS, and media generation.

Mitigation: Install only when broad SkillBoss API access is intended, and review requested actions as external API calls rather than transcript-only operations.

Risk: Prompts, documents, audio, image URLs, email addresses, and phone numbers may be sent to third-party services through SkillBoss API calls.

Mitigation: Avoid sensitive inputs unless the deployment has appropriate data handling controls and user consent for third-party processing.

Risk: Email and SMS actions can contact external recipients.

Mitigation: Require explicit user approval and verify recipients before allowing communication actions.

## Reference(s):

- [Pub Youtube on ClawHub](https://clawhub.ai/abeltennyson/skills/youtube-watchers)
- [SkillBoss API](https://api.heybossai.com/v1)
- [SkillBoss](https://www.skillboss.co)
- [Audio Models](artifact/audio-models.md)
- [Chat Models](artifact/chat-models.md)
- [Image Models](artifact/image-models.md)
- [Search & Scraping Models](artifact/search-models.md)
- [Tool Models](artifact/tools-models.md)
- [Video Models](artifact/video-models.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for authenticated SkillBoss API calls.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
