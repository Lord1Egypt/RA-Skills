## Description: <br>
Swiss-knife for AI agents with 50+ models for image generation, video generation, text-to-speech, speech-to-text, music, chat, web search, document parsing, email, and SMS, plus smart routing for cost saving. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yshuolu](https://clawhub.ai/user/yshuolu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to discover and call SkillBoss/HeyBossAI API models for multimodal generation, chat, web search, document processing, communication, embeddings, and presentation tasks through documented curl patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Data sent through SkillBoss/HeyBossAI may be processed by downstream providers. <br>
Mitigation: Install only if you trust SkillBoss/HeyBossAI and its downstream providers with the data you send; use a limited API key when available. <br>
Risk: Email, batch email, SMS notification, batch SMS, and OTP actions can contact real recipients. <br>
Mitigation: Require manual approval before any email, batch email, SMS notification, batch SMS, or OTP action, and set spending or feature limits where available. <br>


## Reference(s): <br>
- [SkillBoss ClawHub Release](https://clawhub.ai/yshuolu/skillboss-mini) <br>
- [SkillBoss Website](https://www.skillboss.co) <br>
- [HeyBossAI API Base](https://api.heybossai.com/v1) <br>
- [Models Endpoint](https://api.heybossai.com/v1/models) <br>
- [chat-models.md](chat-models.md) <br>
- [image-models.md](image-models.md) <br>
- [audio-models.md](audio-models.md) <br>
- [video-models.md](video-models.md) <br>
- [search-models.md](search-models.md) <br>
- [tools-models.md](tools-models.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls, code] <br>
**Output Format:** [Markdown with curl examples, model tables, endpoint guidance, and JSON request patterns.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and may produce API responses such as text, image URLs, video URLs, audio URLs, markdown, structured JSON, emails, SMS messages, embeddings, or generated presentations depending on the selected model.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
