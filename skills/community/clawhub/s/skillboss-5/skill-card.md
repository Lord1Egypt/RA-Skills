## Description: <br>
Swiss-knife for AI agents. 50+ models for image generation, video generation, text-to-speech, speech-to-text, music, chat, web search, document parsing, email, and SMS with smart routing for cost saving. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MarjorieBroad](https://clawhub.ai/user/MarjorieBroad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use Skillboss to call a multi-provider AI gateway for chat, image, video, audio, search, document processing, email, and SMS tasks through curl commands and a SkillBoss API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private prompts, documents, audio, images, or other content may be sent to outside services through the gateway. <br>
Mitigation: Use a dedicated limited SkillBoss API key and avoid confidential, regulated, or secret data unless external processing is acceptable. <br>
Risk: Email, SMS, OTP, batch, or high-cost actions can affect real users or incur costs. <br>
Mitigation: Require explicit approval before every real-world messaging, verification, batch, or high-cost action. <br>
Risk: Broad model routing can select different external providers and produce outputs with varying quality or safety characteristics. <br>
Mitigation: Review model choices, generated commands, and returned content before using results in downstream workflows. <br>


## Reference(s): <br>
- [SkillBoss API](https://api.heybossai.com/v1) <br>
- [SkillBoss Website](https://www.skillboss.co) <br>
- [ClawHub Skillboss Release](https://clawhub.ai/MarjorieBroad/skillboss-5) <br>
- [Chat Models](artifact/chat-models.md) <br>
- [Image Models](artifact/image-models.md) <br>
- [Video Models](artifact/video-models.md) <br>
- [Audio Models](artifact/audio-models.md) <br>
- [Search and Scraping Models](artifact/search-models.md) <br>
- [Tool Models](artifact/tools-models.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl examples, model IDs, request parameters, and response fields.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
