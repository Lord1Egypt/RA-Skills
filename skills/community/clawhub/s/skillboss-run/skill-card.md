## Description:

Multi-AI gateway. 50+ models: chat, image, video, TTS, music, search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yshuolu](https://clawhub.ai/user/yshuolu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use Skillboss to list available models, route prompts to selected chat and media models, and auto-select models for common chat, image, and text-to-speech tasks through the SkillBoss gateway.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, task inputs, and the SkillBoss API key are sent to the SkillBoss/HeyBoss remote API and may be routed to downstream model providers.

Mitigation: Use only with data your organization permits sharing with the remote service; avoid submitting secrets, regulated data, or proprietary content unless approved.

## Reference(s):

- [Skillboss ClawHub page](https://clawhub.ai/yshuolu/skills/skillboss-run)
- [SkillBoss](https://www.skillboss.co)
- [SkillBoss models API](https://api.heybossai.com/v1/models)
- [SkillBoss run API](https://api.heybossai.com/v1/run)
- [SkillBoss pilot API](https://api.heybossai.com/v1/pilot)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Media URLs, Guidance]

**Output Format:** [Plain text, JSON, or URL strings printed by a Node.js command-line script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and the SKILLBOSS_API_KEY environment variable; prompts, task inputs, and API key are sent to the SkillBoss/HeyBoss remote API.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
