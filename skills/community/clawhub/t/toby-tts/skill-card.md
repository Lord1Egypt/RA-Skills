## Description:

Convert text to speech using SkillBoss API Hub for audio messages, voice replies, or requests to hear supplied text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to turn supplied text into MP3 voice messages through the SkillBoss API Hub, then return the generated audio file to the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text submitted for speech generation is sent to the SkillBoss/HeyBossAI remote service.

Mitigation: Do not convert secrets or sensitive private data, and use the skill only when remote TTS processing is acceptable.

Risk: The script requires SKILLBOSS_API_KEY in its environment.

Mitigation: Use a scoped key where possible and avoid exposing the key in shared logs, shell history, or committed files.

Risk: The output path is caller-controlled and can overwrite writable files.

Mitigation: Write only to a dedicated output directory with non-sensitive filenames and review paths before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobeyrebecca/skills/toby-tts)
- [Publisher profile](https://clawhub.ai/user/tobeyrebecca)
- [SkillBoss API Hub endpoint](https://api.heybossai.com/v1)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [MP3 audio file plus console text that includes a MEDIA path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and a caller-selected output path]

## Skill Version(s):

1.0.0 (source: server release metadata and scripts/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
