## Description: <br>
Provides SkillBoss API guidance for chat, image, video, audio, search, scraping, document, email, and SMS capabilities, with a stated goal of capturing learnings for agent improvement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[QuincyGunter](https://clawhub.ai/user/QuincyGunter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to access SkillBoss-hosted model and tool endpoints through documented shell commands and JSON payloads. It is suited for workflows that need multi-provider model calls, generated media, search, scraping, document processing, email, or SMS actions from an agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent access to a broad API gateway that includes email, SMS, OTP, scraping, and document-processing actions. <br>
Mitigation: Use a limited SkillBoss API key where possible and require explicit user approval before email, SMS, OTP, scraping, or document-processing calls. <br>
Risk: Requests may send confidential documents, personal data, prompts, or media to external provider chains. <br>
Mitigation: Avoid confidential or personal data unless the provider chain is trusted and the user has approved the disclosure. <br>
Risk: The release is presented as a self-improving-agent skill but primarily behaves as a broad SkillBoss API gateway. <br>
Mitigation: Install it only when broad SkillBoss gateway access is intended, and review the action scope before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/QuincyGunter/self-improve-agent) <br>
- [SkillBoss API base URL](https://api.heybossai.com/v1) <br>
- [SkillBoss API key signup](https://www.skillboss.co) <br>
- [Chat model reference](artifact/chat-models.md) <br>
- [Image model reference](artifact/image-models.md) <br>
- [Video model reference](artifact/video-models.md) <br>
- [Audio model reference](artifact/audio-models.md) <br>
- [Search and scraping model reference](artifact/search-models.md) <br>
- [Tool model reference](artifact/tools-models.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Files] <br>
**Output Format:** [Markdown guidance with bash/curl examples and JSON API payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY; API responses may include text, URLs, binary media, or generated files depending on the selected model.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
