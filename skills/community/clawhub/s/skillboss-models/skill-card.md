## Description:

Multi-AI gateway for agents. 50+ models: chat, image, video, TTS, STT, music, search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yshuolu](https://clawhub.ai/user/yshuolu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use Skillboss to list and run multiple AI model types through a single SkillBoss API key, including chat, image, video, text-to-speech, speech-to-text, music, and search tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys, prompts, chat context, text, and media URLs may be sent to the SkillBoss/HeyBossAI remote service.

Mitigation: Use the skill only when that sharing is intended; avoid sensitive proprietary data unless approved.

Risk: The skill requires a SkillBoss API key for remote model calls.

Mitigation: Use a dedicated, revocable key with spending limits and rotate or revoke it when no longer needed.

Risk: Generated media may be returned as URLs for separate download.

Mitigation: Save downloaded media to a non-conflicting filename or output folder and review outputs before reuse.

## Reference(s):

- [ClawHub Skillboss listing](https://clawhub.ai/yshuolu/skills/skillboss-models)
- [Publisher profile](https://clawhub.ai/user/yshuolu)
- [SkillBoss](https://www.skillboss.co)
- [SkillBoss API base](https://api.heybossai.com/v1)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Terminal text, JSON, or media URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and SKILLBOSS_API_KEY; media generation responses may be returned as URLs for separate download.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
