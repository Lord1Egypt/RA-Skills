## Description: <br>
Provides agent guidance for calling SkillBoss APIs across chat, image, video, audio, search, document processing, email, and SMS tasks; the release is presented as video-frame extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MartinPollitt](https://clawhub.ai/user/MartinPollitt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to produce command and API-call guidance for SkillBoss model tasks, including media generation, chat, search, scraping, document processing, email, and SMS. Review is important because the artifact exposes broader external actions than the video-frame title suggests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release title suggests video-frame extraction, while the artifact documents a broad external API gateway. <br>
Mitigation: Install only when the broad SkillBoss API surface is intended, not solely for local video-frame extraction. <br>
Risk: The skill can guide actions that send prompts, media, documents, contact details, or verification data to external services. <br>
Mitigation: Use a restricted API key when available and avoid sending sensitive data unless the provider and destination are trusted. <br>
Risk: Email, SMS, batch messaging, scraping, and paid model actions can have user-impacting or cost-bearing effects. <br>
Mitigation: Require manual approval before those actions are executed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/MartinPollitt/video-framess) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Audio Models](artifact/audio-models.md) <br>
- [Chat Models](artifact/chat-models.md) <br>
- [Image Models](artifact/image-models.md) <br>
- [Search & Scraping Models](artifact/search-models.md) <br>
- [Tool Models](artifact/tools-models.md) <br>
- [Video Models](artifact/video-models.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for live API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
