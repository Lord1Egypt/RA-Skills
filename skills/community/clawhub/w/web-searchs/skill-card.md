## Description: <br>
Search the web for current information and news, and access SkillBoss models for chat, image, video, audio, document, email, and SMS workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KirkRaman](https://clawhub.ai/user/KirkRaman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to discover and call SkillBoss API models for web search, current-content retrieval, multimodal generation, document processing, and outbound messaging tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill provides broad SkillBoss API access beyond web search, including email and SMS capabilities. <br>
Mitigation: Install only when broad gateway access is intended, and use a constrained API key or spending limits where available. <br>
Risk: Requests may send sensitive documents, audio, recipient details, or other user data to SkillBoss and downstream providers. <br>
Mitigation: Avoid sensitive inputs unless the service and downstream providers are trusted for the use case. <br>
Risk: Email, SMS, OTP, and batch messaging actions can contact external recipients. <br>
Mitigation: Require explicit human approval before any outbound messaging or verification action. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/KirkRaman/web-searchs) <br>
- [Publisher Profile](https://clawhub.ai/user/KirkRaman) <br>
- [SkillBoss API Base URL](https://api.heybossai.com/v1) <br>
- [SkillBoss](https://www.skillboss.co) <br>
- [Search & Scraping Models](artifact/search-models.md) <br>
- [Tool Models](artifact/tools-models.md) <br>
- [Chat Models](artifact/chat-models.md) <br>
- [Image Models](artifact/image-models.md) <br>
- [Audio Models](artifact/audio-models.md) <br>
- [Video Models](artifact/video-models.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash/curl examples and JSON request payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY; API responses vary by selected model and may include text, search results, generated media URLs, parsed documents, or messaging action results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
