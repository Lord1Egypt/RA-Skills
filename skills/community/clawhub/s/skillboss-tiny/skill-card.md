## Description:

Multi-AI gateway. 50+ models: chat, image, video, TTS, music, search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marjoriebroad](https://clawhub.ai/user/marjoriebroad)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to discover available SkillBoss models and route prompts for chat, image, video, text-to-speech, speech-to-text, music, and web search tasks through a single API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and the SkillBoss API key are sent to an external API at api.heybossai.com, which differs from the SkillBoss branding.

Mitigation: Review the relationship between skillboss.co and api.heybossai.com before installing, and use a limited, revocable API key with spending or rate limits where possible.

Risk: Sensitive prompts may leave the user's environment and be processed by external services and downstream providers.

Mitigation: Avoid sending secrets, regulated personal data, proprietary code, or confidential business content unless the external service and its downstream providers are trusted.

## Reference(s):

- [SkillBoss website](https://www.skillboss.co)
- [HeyBoss AI API endpoint](https://api.heybossai.com/v1)
- [ClawHub skill page](https://clawhub.ai/marjoriebroad/skills/skillboss-tiny)
- [Publisher profile](https://clawhub.ai/user/marjoriebroad)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Terminal text, JSON responses, media URLs, and Markdown command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and the SKILLBOSS_API_KEY environment variable.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
