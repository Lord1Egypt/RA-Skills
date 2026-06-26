## Description: <br>
Get current weather and forecasts, plus access to a broad SkillBoss API gateway for model, search, scraping, document, email, and SMS actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AbelTennyson](https://clawhub.ai/user/AbelTennyson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call SkillBoss-hosted weather, model, search, scraping, document, email, and SMS capabilities through one API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is labeled as weather-focused but exposes a broad external API gateway. <br>
Mitigation: Install only when the agent is expected to access broad SkillBoss capabilities, not only weather. <br>
Risk: The gateway can trigger sensitive or high-impact actions such as email, SMS, OTP, scraping, document processing, and paid model calls. <br>
Mitigation: Require explicit approval before these actions and use restricted, revocable API keys where possible. <br>
Risk: Prompts, files, audio, URLs, or other user data may be sent to external providers through the gateway. <br>
Mitigation: Avoid sending sensitive data through the skill unless the deployment has approved the relevant providers and data handling terms. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AbelTennyson/weather-hub) <br>
- [SkillBoss website](https://www.skillboss.co) <br>
- [SkillBoss API base](https://api.heybossai.com/v1) <br>
- [SkillBoss models endpoint](https://api.heybossai.com/v1/models) <br>
- [Chat Models](artifact/chat-models.md) <br>
- [Image Models](artifact/image-models.md) <br>
- [Video Models](artifact/video-models.md) <br>
- [Audio Models](artifact/audio-models.md) <br>
- [Search & Scraping Models](artifact/search-models.md) <br>
- [Tool Models](artifact/tools-models.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for SkillBoss API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
