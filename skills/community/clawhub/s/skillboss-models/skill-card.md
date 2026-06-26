## Description: <br>
Multi-AI gateway for agents. 50+ models: chat, image, video, TTS, STT, music, search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yshuolu](https://clawhub.ai/user/yshuolu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Skillboss to discover and call chat, image, video, text-to-speech, speech-to-text, music, and search models through a single API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, text, image URLs, context, and the API key are sent to a remote SkillBoss/HeyBossAI service. <br>
Mitigation: Use only with trusted data and confirm the provider's privacy and retention terms before submitting secrets or sensitive internal content. <br>
Risk: Generated image, video, audio, and TTS results may be returned as remote media URLs. <br>
Mitigation: Treat returned media URLs as untrusted remote content; download only intentionally, save to a safe location, and review files before reuse. <br>


## Reference(s): <br>
- [Skillboss ClawHub release](https://clawhub.ai/yshuolu/skillboss-models) <br>
- [SkillBoss API key portal](https://www.skillboss.co) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Command-line output as plain text, JSON, or media URLs; guidance is Markdown with bash examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and SKILLBOSS_API_KEY; remote model responses and media URLs depend on the selected model or task.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
