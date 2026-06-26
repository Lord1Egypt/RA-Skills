## Description: <br>
Swiss-knife for AI agents. 50+ models for image generation, video generation, text-to-speech, speech-to-text, music, chat, web search, document parsing, email, and SMS, with smart routing for cost saving. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yshuolu](https://clawhub.ai/user/yshuolu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use Skillboss to discover and call a broad remote API gateway for chat, image, video, audio, search, scraping, document processing, email, SMS, embeddings, and presentation generation. It provides cURL-based request patterns and model lists for direct model selection or smart routing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables broad remote API access, including email, SMS, OTP, document, and audio-processing workflows. <br>
Mitigation: Install only when SkillBoss is trusted as a remote gateway, use restricted or budget-limited credentials where possible, and require explicit human review before email, SMS, OTP, or batch communication is sent. <br>
Risk: Documents, recordings, or generated content may be sent to remote services through the SkillBoss API. <br>
Mitigation: Avoid confidential documents or recordings unless the user is authorized to process them through this service. <br>
Risk: The skill depends on a live API key with access to paid or sensitive model providers. <br>
Mitigation: Store SKILLBOSS_API_KEY securely, scope it where supported, and monitor usage for unexpected cost or access patterns. <br>


## Reference(s): <br>
- [ClawHub Skillboss listing](https://clawhub.ai/yshuolu/skillboss-swissknife) <br>
- [SkillBoss API base URL](https://api.heybossai.com/v1) <br>
- [SkillBoss website](https://www.skillboss.co) <br>
- [Audio Models](artifact/audio-models.md) <br>
- [Chat Models](artifact/chat-models.md) <br>
- [Image Models](artifact/image-models.md) <br>
- [Search and Scraping Models](artifact/search-models.md) <br>
- [Tool Models](artifact/tools-models.md) <br>
- [Video Models](artifact/video-models.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with cURL commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for live API calls.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
