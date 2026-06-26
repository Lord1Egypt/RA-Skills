## Description: <br>
Multi-AI gateway. 50+ models: chat, image, video, TTS, music, search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MarjorieBroad](https://clawhub.ai/user/MarjorieBroad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use Skillboss to discover and call SkillBoss/HeyBoss models for chat, image, video, text-to-speech, speech-to-text, music, and web search through a Node-based command workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and task inputs are sent to the external SkillBoss/HeyBoss service. <br>
Mitigation: Use only data approved for that provider and avoid confidential or regulated content unless the provider terms and controls are acceptable. <br>
Risk: SKILLBOSS_API_KEY is required and may expose account usage or billing if mishandled. <br>
Mitigation: Store the key as a secret, avoid printing it, and monitor API usage or billing. <br>


## Reference(s): <br>
- [ClawHub Skillboss release](https://clawhub.ai/MarjorieBroad/skillboss-tiny) <br>
- [SkillBoss website](https://www.skillboss.co) <br>
- [HeyBoss API endpoint](https://api.heybossai.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, JSON, Media URLs, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands; command output may be JSON, plain text, or downloadable media URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and SKILLBOSS_API_KEY; sends prompts to the SkillBoss/HeyBoss external API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
