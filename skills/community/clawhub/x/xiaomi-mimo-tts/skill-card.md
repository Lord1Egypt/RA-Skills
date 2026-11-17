## Description:

Generates speech with Xiaomi MiMo TTS (mimo-v2-tts), supporting multiple voices, style controls, emotion tags, and dialect cues through a Xiaomi MiMo API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jazzqi](https://clawhub.ai/user/jazzqi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to turn text into Xiaomi MiMo-generated speech and optionally apply style, emotion, speed, or dialect cues for conversational audio output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text submitted for synthesis is sent to Xiaomi's MiMo API using the configured API key.

Mitigation: Only synthesize content appropriate for that service, and avoid sending sensitive or untrusted text without approval.

Risk: Security evidence reports a local code-execution flaw in bundled scripts, including the shell dry-run path.

Mitigation: Review or patch the scripts before execution, and do not pass untrusted text through dry-run shell behavior until fixed.

Risk: The documentation includes unpinned npx and pip install examples.

Mitigation: Pin and verify exact package versions before installing or running dependencies.

Risk: Generated audio can be written to caller-selected output paths.

Mitigation: Constrain outputs to a dedicated audio directory such as SKILL_OUT and clean generated files after use.

## Reference(s):

- [ClawHub Xiaomi MiMo TTS skill page](https://clawhub.ai/jazzqi/skills/xiaomi-mimo-tts)
- [Xiaomi MiMo platform](https://platform.xiaomimimo.com/)
- [Xiaomi MiMo chat completions API endpoint](https://api.xiaomimimo.com/v1/chat/completions)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions]

**Output Format:** [Audio file paths and shell status text; dry-run mode can print JSON payload previews]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires XIAOMI_API_KEY or MIMO_API_KEY; writes OGG or WAV audio outputs and may use ffmpeg for conversion.]

## Skill Version(s):

1.2.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
