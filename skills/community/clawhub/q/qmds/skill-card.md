## Description: <br>
Pub Qmd provides command examples for using SkillBoss as a broad remote API gateway to 50+ models across chat, image, video, audio, search, document processing, email, and SMS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GodferyLindsay](https://clawhub.ai/user/GodferyLindsay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to discover SkillBoss models and prepare API calls for chat, media generation, search, scraping, document processing, email, and SMS workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can route prompts, documents, and generated requests through a broad third-party API gateway. <br>
Mitigation: Use a scoped, revocable SKILLBOSS_API_KEY and avoid sensitive documents or private prompts unless the provider is trusted for the intended data. <br>
Risk: The skill includes email, SMS, OTP, scraping, and document-processing capabilities that can affect external systems or third parties. <br>
Mitigation: Require explicit human confirmation before email, SMS, OTP, scraping, or document-processing actions are executed. <br>
Risk: The release is partly described as local search/indexing while the security evidence identifies broad remote API behavior. <br>
Mitigation: Review the artifact as a remote API integration before installation and verify that this behavior matches the deployment intent. <br>


## Reference(s): <br>
- [Pub Qmd ClawHub Listing](https://clawhub.ai/GodferyLindsay/qmds) <br>
- [SkillBoss Website](https://www.skillboss.co) <br>
- [SkillBoss API Base URL](https://api.heybossai.com/v1) <br>
- [Chat Models](artifact/chat-models.md) <br>
- [Image Models](artifact/image-models.md) <br>
- [Audio Models](artifact/audio-models.md) <br>
- [Video Models](artifact/video-models.md) <br>
- [Search & Scraping Models](artifact/search-models.md) <br>
- [Tool Models](artifact/tools-models.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with curl and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and sends requests to third-party remote APIs.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
