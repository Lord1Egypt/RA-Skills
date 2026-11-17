## Description:

Provides agents with curl-based guidance for using the SkillBoss API across chat, image, video, audio, search, document processing, email, SMS, and model discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abeltennyson](https://clawhub.ai/user/abeltennyson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to have an agent discover SkillBoss models and prepare API calls for model execution, web search and scraping, document processing, media generation, and communication tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package is labeled as a weather skill, but the evidence describes a broad SkillBoss API gateway with model calls, scraping, document and media processing, email, and SMS capabilities.

Mitigation: Review it as a broad API gateway and install it only when those capabilities are intended for the agent workflow.

Risk: SkillBoss API calls require SKILLBOSS_API_KEY and can spend quota or access third-party provider capabilities.

Mitigation: Store the key as an approved secret, scope access where possible, and require explicit approval before agent-initiated API calls.

Risk: Email and SMS actions can contact external recipients.

Mitigation: Require explicit user confirmation of recipients, message contents, and purpose before sending communication requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abeltennyson/skills/weather-hub)
- [SkillBoss website](https://www.skillboss.co)
- [SkillBoss API base endpoint](https://api.heybossai.com/v1)
- [Audio models](artifact/audio-models.md)
- [Chat models](artifact/chat-models.md)
- [Image models](artifact/image-models.md)
- [Search and scraping models](artifact/search-models.md)
- [Tool models](artifact/tools-models.md)
- [Video models](artifact/video-models.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for authenticated SkillBoss API calls.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
