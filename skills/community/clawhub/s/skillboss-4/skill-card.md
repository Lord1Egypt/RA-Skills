## Description: <br>
Swiss-knife for AI agents with 50+ models for image generation, video generation, text-to-speech, speech-to-text, music, chat, web search, document parsing, email, and SMS, plus smart routing for cost savings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MarjorieBroad](https://clawhub.ai/user/MarjorieBroad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Skillboss to route agent tasks through SkillBoss for chat, image, video, audio, search, scraping, document processing, email, and SMS workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task data is sent through SkillBoss and downstream providers. <br>
Mitigation: Avoid secrets or regulated data unless approved for those services, and review prompts before sending. <br>
Risk: Model calls, scraping, email, SMS, and profile lookup actions may incur costs or affect third parties. <br>
Mitigation: Use a scoped or low-budget API key, monitor usage, and confirm recipients or targets before running those actions. <br>


## Reference(s): <br>
- [Skillboss ClawHub listing](https://clawhub.ai/MarjorieBroad/skillboss-4) <br>
- [MarjorieBroad publisher profile](https://clawhub.ai/user/MarjorieBroad) <br>
- [SkillBoss website](https://www.skillboss.co) <br>
- [Chat Models](artifact/chat-models.md) <br>
- [Image Models](artifact/image-models.md) <br>
- [Video Models](artifact/video-models.md) <br>
- [Audio Models](artifact/audio-models.md) <br>
- [Search and Scraping Models](artifact/search-models.md) <br>
- [Tool Models](artifact/tools-models.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Media URLs] <br>
**Output Format:** [Plain text, JSON, or URLs printed by the Node command wrapper] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and SKILLBOSS_API_KEY; external provider calls may incur costs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
