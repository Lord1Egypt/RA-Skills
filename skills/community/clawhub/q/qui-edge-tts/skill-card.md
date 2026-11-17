## Description:

Converts text to speech through the SkillBoss API Hub TTS service, with options for voice, language, speed, pitch, volume, output files, and subtitles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quincygunter](https://clawhub.ai/user/quincygunter)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to generate spoken audio from text for accessibility, multitasking, voice notes, summaries, and customized text-to-speech workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text submitted for conversion may be sent to the external SkillBoss/HeyBossAI TTS service.

Mitigation: Use the skill only with text that is acceptable to share with that service, and avoid sensitive or regulated content unless the deployment has approved that data flow.

Risk: The required SKILLBOSS_API_KEY could be exposed through logs, shell history, or shared environments.

Mitigation: Store the key in a secret manager or protected environment variable, avoid echoing it in shared shells, and rotate it if exposure is suspected.

Risk: Generated audio files and TTS configuration can persist on disk.

Mitigation: Clean generated audio files after use and review stored configuration, especially on shared machines.

Risk: Dependency installation behavior may be difficult to review when using unpinned examples or stale lockfile entries.

Mitigation: Use a locked dependency install, avoid unpinned npx examples, and review or remove stale node-edge-tts lockfile entries before deployment.

## Reference(s):

- [Node Edge TTS Guide](references/node_edge_tts_guide.md)
- [Voice Testing](https://tts.travisvn.com/)
- [ClawHub Skill Page](https://clawhub.ai/quincygunter/skills/qui-edge-tts)
- [Publisher Profile](https://clawhub.ai/user/quincygunter)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration, Guidance]

**Output Format:** [Audio files with markdown and inline shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can persist TTS configuration and generated audio files; requires SKILLBOSS_API_KEY and internet access.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata; artifact package metadata reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
