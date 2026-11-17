## Description:

Generate WAV speech audio from text using Xiaomi MiMo TTS (mimo-v2-tts), with preset voices, style controls, and audio tags for expression.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heimaojingzhang888](https://clawhub.ai/user/heimaojingzhang888)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to synthesize text into local WAV files through Xiaomi MiMo TTS, including styled Chinese or English speech for read-aloud and voice-file workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text to synthesize, optional context, and the MiMo API key are sent to Xiaomi MiMo's API.

Mitigation: Use the skill only when that data sharing is acceptable, and avoid secrets, private records, or sensitive personal content unless it matches the user's data-sharing expectations.

Risk: The script writes synthesized audio to a local output path.

Mitigation: Choose an intentional output path and review generated audio before using or distributing it.

## Reference(s):

- [Xiaomi MiMo API](https://api.xiaomimimo.com)
- [ClawHub skill page](https://clawhub.ai/heimaojingzhang888/skills/xiaomimimotts)
- [Publisher profile](https://clawhub.ai/user/heimaojingzhang888)

## Skill Output:

**Output Type(s):** [files, shell commands, configuration, guidance]

**Output Format:** [WAV audio file plus concise command and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MIMO_API_KEY; sends text and optional context to Xiaomi MiMo API; supports voice, style, output path, and WAV format options.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
