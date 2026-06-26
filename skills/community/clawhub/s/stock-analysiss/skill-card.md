## Description: <br>
Analyzes stocks and cryptocurrencies using Yahoo Finance data while exposing SkillBoss gateway commands for chat, media generation, search, document processing, email, and SMS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KirkRaman](https://clawhub.ai/user/KirkRaman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run stock and cryptocurrency analysis workflows and invoke SkillBoss model/API gateway commands for content generation, search, document processing, and communications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package is presented as stock analysis but enables a broad SkillBoss API gateway, including AI, scraping, email, SMS, document, audio, and media actions. <br>
Mitigation: Install only when that broad gateway is intended, use a restricted or dedicated SKILLBOSS_API_KEY, and monitor usage and costs. <br>
Risk: Email, SMS, document, audio, phone number, verification code, and private URL inputs may be sent through SkillBoss and downstream providers. <br>
Mitigation: Require explicit confirmation before email or SMS actions and avoid sending sensitive data unless the user trusts SkillBoss and the downstream providers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/KirkRaman/stock-analysiss) <br>
- [Publisher profile](https://clawhub.ai/user/KirkRaman) <br>
- [SkillBoss API](https://api.heybossai.com/v1) <br>
- [SkillBoss](https://www.skillboss.co) <br>
- [Audio Models](audio-models.md) <br>
- [Chat Models](chat-models.md) <br>
- [Image Models](image-models.md) <br>
- [Search & Scraping Models](search-models.md) <br>
- [Tool Models](tools-models.md) <br>
- [Video Models](video-models.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for SkillBoss API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
