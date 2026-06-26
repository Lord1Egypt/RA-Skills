## Description: <br>
Control Slack from Clawdbot including reacting to messages and pinning items, plus access to SkillBoss models for image, video, audio, chat, web search, document parsing, email, and SMS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KirkRaman](https://clawhub.ai/user/KirkRaman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to issue Slack-related actions and call SkillBoss-hosted model and tool APIs from an agent workflow. It is suited for teams that intentionally grant a broad SkillBoss API key for multimodal generation, search, document processing, email, and SMS tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Slack-labeled skill grants broad SkillBoss API access beyond Slack automation, including email, SMS, document parsing, and smart-routed provider actions. <br>
Mitigation: Install only when that broad access is intended, scope and protect SKILLBOSS_API_KEY, and require explicit human approval before email, SMS, OTP, batch messaging, document parsing, or smart-routed actions. <br>
Risk: Workplace content or sensitive documents may be sent to external processing services through the SkillBoss API. <br>
Mitigation: Avoid sending sensitive workplace content unless external processing is approved for the deployment context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/KirkRaman/slack-ai) <br>
- [Publisher profile](https://clawhub.ai/user/KirkRaman) <br>
- [SkillBoss API base URL](https://api.heybossai.com/v1) <br>
- [SkillBoss website](https://www.skillboss.co) <br>
- [Chat model reference](chat-models.md) <br>
- [Image model reference](image-models.md) <br>
- [Video model reference](video-models.md) <br>
- [Audio model reference](audio-models.md) <br>
- [Search and scraping model reference](search-models.md) <br>
- [Tool model reference](tools-models.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with curl examples, parameter tables, and environment-variable requirements] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY; outputs may include generated media URLs, text, markdown, JSON-like API responses, files, email, or SMS actions depending on the selected model.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
