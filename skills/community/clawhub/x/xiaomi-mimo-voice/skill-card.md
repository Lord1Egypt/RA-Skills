## Description:

Provides Xiaomi MiMo V2 text-to-speech generation for Chinese and English speech with emotion, role-play, dialect, speed, and narration style controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luhuiwang](https://clawhub.ai/user/luhuiwang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to synthesize speech from supplied text through the Xiaomi MiMo V2 TTS API, selecting voice, style, dialect, and output format as needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted TTS text is sent to Xiaomi's API and may contain sensitive content.

Mitigation: Do not submit secrets, private personal data, or regulated content unless sharing it with Xiaomi is acceptable.

Risk: The skill depends on API credentials for outbound requests.

Mitigation: Store MIMO_API_KEY in the intended skill configuration or environment and avoid exposing it in prompts, logs, or shared files.

Risk: Installation and dependency commands may retrieve mutable packages.

Mitigation: Install in a normal non-admin environment and review the package source before using npx or pip commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luhuiwang/skills/xiaomi-mimo-voice)
- [Xiaomi MiMo API endpoint](https://api.xiaomimimo.com/v1/chat/completions)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions]

**Output Format:** [Audio file in WAV or PCM16 format with JSON status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MIMO_API_KEY and sends submitted text to Xiaomi's API.]

## Skill Version(s):

1.0.4 (source: server release evidence; artifact frontmatter and changelog show 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
