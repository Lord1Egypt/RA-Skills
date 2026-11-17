## Description:

Pub Qmd provides agent-facing SkillBoss API examples for local search/indexing and for routing requests across chat, image, video, audio, search, document, email, and SMS models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[godferylindsay](https://clawhub.ai/user/godferylindsay)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to discover SkillBoss models and construct authenticated API calls for model inference, media generation, search and scraping, document processing, email, and SMS workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send prompts, media, documents, and other task data to SkillBoss and downstream providers.

Mitigation: Provide SKILLBOSS_API_KEY only in environments approved for external API use, and redact sensitive data before invoking remote models.

Risk: Email, SMS, batch messaging, audio, image, and document-processing calls can create external side effects or expose user data.

Mitigation: Require explicit user direction before side-effecting calls and review destinations, content, attachments, and generated requests before execution.

Risk: The artifact describes local search/indexing while also exposing a broad remote API wrapper, which can obscure the true execution posture.

Mitigation: Document operational boundaries during deployment and limit agent access to the specific model categories needed for the approved use case.

## Reference(s):

- [SkillBoss API Base URL](https://api.heybossai.com/v1)
- [SkillBoss Models Endpoint](https://api.heybossai.com/v1/models)
- [SkillBoss Website](https://www.skillboss.co)
- [Chat Models](chat-models.md)
- [Image Models](image-models.md)
- [Video Models](video-models.md)
- [Audio Models](audio-models.md)
- [Search and Scraping Models](search-models.md)
- [Tool Models](tools-models.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown guidance with curl and CLI command examples plus JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY; calls may return text, JSON, media URLs, generated files, or provider-specific API responses.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
