## Description: <br>
Skillboss is a multi-AI gateway for accessing 50+ models across chat, image, video, TTS, music, and search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yshuolu](https://clawhub.ai/user/yshuolu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use Skillboss to list hosted models and route chat, image, video, speech, music, and search tasks through the SkillBoss service with one API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, media-generation requests, and the SkillBoss API key are sent to the external SkillBoss/HeyBossAI service and may be routed onward to model providers. <br>
Mitigation: Use a dedicated revocable API key, avoid secrets or regulated data unless approved by your organization, and monitor account usage and billing. <br>
Risk: Returned model text, JSON, or media URLs may reflect behavior from multiple hosted model providers. <br>
Mitigation: Review outputs before relying on them and apply the organization's safety, privacy, and content policies before using generated results. <br>


## Reference(s): <br>
- [Skillboss ClawHub page](https://clawhub.ai/yshuolu/skillboss-run) <br>
- [SkillBoss website](https://www.skillboss.co) <br>
- [HeyBossAI models endpoint](https://api.heybossai.com/v1/models) <br>
- [HeyBossAI run endpoint](https://api.heybossai.com/v1/run) <br>
- [HeyBossAI pilot endpoint](https://api.heybossai.com/v1/pilot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text, JSON, or URL strings returned by shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and SKILLBOSS_API_KEY; image, video, and audio tasks can return downloadable media URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
