## Description: <br>
Summarize URLs or files with the summarize CLI and access SkillBoss models for generation, transcription, search, document processing, email, and SMS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[QuincyGunter](https://clawhub.ai/user/QuincyGunter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to summarize web pages, files, PDFs, images, audio, and YouTube content, and to call SkillBoss-hosted AI models across multiple providers. It also exposes broader generation, search, document, email, SMS, and smart-routing workflows through API examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review describes this as a broad external API gateway under a summarization name, including email, SMS and OTP, scraping, and smart-routing actions. <br>
Mitigation: Install only when that broad SkillBoss API access is intended, use a restricted API key when available, monitor usage and billing, and require explicit approval before email, SMS, OTP, scraping, or smart-routed actions. <br>
Risk: Inputs and generated outputs may be processed by external providers through SkillBoss. <br>
Mitigation: Avoid sensitive or regulated data unless external processing is acceptable for the deployment context. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/QuincyGunter/smart-summarize) <br>
- [SkillBoss API Base](https://api.heybossai.com/v1) <br>
- [SkillBoss](https://www.skillboss.co) <br>
- [Chat Models](chat-models.md) <br>
- [Image Models](image-models.md) <br>
- [Audio Models](audio-models.md) <br>
- [Search & Scraping Models](search-models.md) <br>
- [Tool Models](tools-models.md) <br>
- [Video Models](video-models.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for API-backed workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
