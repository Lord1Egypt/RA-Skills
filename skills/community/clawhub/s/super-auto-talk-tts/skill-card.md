## Description:

Super Auto Talk Tts converts agent messages into spoken audio using Edge TTS, with configurable voice, speed, pitch, volume, and asynchronous playback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[subaru0573](https://clawhub.ai/user/subaru0573)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to have agent responses spoken aloud automatically for accessibility, hands-free review, or voice-oriented workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to persistently force all future agent messages through automatic background speech generation.

Mitigation: Enable it only for workflows that intentionally require automatic speech, and remove or decline persistent SOUL.md instructions when continuous speech is not desired.

Risk: The skill describes automatic or global npm package installation.

Mitigation: Avoid automatic global installs; review and pin dependencies before installation in a controlled environment.

Risk: The package declares an auto-speak executable, but the artifact does not include that executable file.

Mitigation: Confirm that the executable is supplied from a trusted source before running commands that invoke auto-speak.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/subaru0573/skills/super-auto-talk-tts)
- [Publisher profile](https://clawhub.ai/user/subaru0573)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, spoken audio]

**Output Format:** [Markdown guidance with inline shell commands and generated speech playback]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses configurable voice, rate, pitch, volume, and summary length settings.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact/_meta.json, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
