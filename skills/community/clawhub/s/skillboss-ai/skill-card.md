## Description: <br>
Swiss-knife for AI agents. 50+ models for image generation, video generation, text-to-speech, speech-to-text, music, chat, web search, document parsing, email, and SMS — with smart routing for cost saving. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yshuolu](https://clawhub.ai/user/yshuolu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use SkillBoss to route prompts, files, and task requests through a single API for chat, image, video, audio, search, document parsing, email, SMS, embeddings, and presentation generation. It supports both direct model calls by ID and smart routing by task with price, quality, or balanced preferences. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, files, URLs, generated outputs, and local audio files may be sent to SkillBoss and downstream model providers. <br>
Mitigation: Use the skill only with data appropriate for those providers, avoid secrets and regulated data, and review outbound inputs before execution. <br>
Risk: API keys can be read from the environment or saved config, and the auth flow can write credentials to config.json. <br>
Mitigation: Prefer SKILLBOSS_API_KEY from a secure environment, avoid committing config.json with real credentials, and use logout or secret rotation when needed. <br>
Risk: Email and SMS models can send messages, including batch sends, through remote providers. <br>
Mitigation: Require explicit human review and approval before invoking email or SMS models, especially for batch operations. <br>


## Reference(s): <br>
- [ClawHub SkillBoss Release](https://clawhub.ai/yshuolu/skillboss-ai) <br>
- [SkillBoss Publisher Profile](https://clawhub.ai/user/yshuolu) <br>
- [SkillBoss Website](https://www.skillboss.co) <br>
- [API Integration](artifact/api-integration.md) <br>
- [Error Handling](artifact/error-handling.md) <br>
- [Chat Models](artifact/chat-models.md) <br>
- [Image Models](artifact/image-models.md) <br>
- [Audio Models](artifact/audio-models.md) <br>
- [Search & Scraping Models](artifact/search-models.md) <br>
- [Tool Models](artifact/tools-models.md) <br>
- [Video Models](artifact/video-models.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Plain text, JSON, Markdown, generated media files, and saved local output files depending on the selected model or task.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write image, video, and audio outputs to user-specified paths; speech-to-text and chat results are printed to stdout.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
