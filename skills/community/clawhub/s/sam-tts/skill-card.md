## Description:

Generate retro robotic speech audio using SAM (Software Automatic Mouth), with one-time /sam messages, optional persistent SAM mode, and pitch, speed, mouth, and throat controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fourthdensity](https://clawhub.ai/user/fourthdensity)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use SAM TTS to convert chat responses or /sam command text into retro C64-style WAV audio. The skill can also persist a user-controlled SAM mode setting and adjust voice parameters for future generated audio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SAM mode persists a local setting and can turn future responses into generated WAV audio until disabled.

Mitigation: Keep mode state limited to memory/sam-mode.json, support /sam status and /sam off, and make mode changes explicit to the user.

Risk: The wrapper writes generated WAV files to a caller-provided output path.

Mitigation: Use explicit output paths in temporary or user-approved locations and avoid overwriting important files.

Risk: The package manifest permits compatible sam-js dependency updates while the current lockfile is pinned.

Mitigation: Review dependency updates normally and refresh security review when changing the lockfile or dependency version.

## Reference(s):

- [SAM JavaScript dependency](https://github.com/discordier/sam)
- [sam-js package archive](https://registry.npmjs.org/sam-js/-/sam-js-0.3.1.tgz)
- [ClawHub skill page](https://clawhub.ai/fourthdensity/skills/sam-tts)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, audio files]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output; generated audio is WAV.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated WAV output is 22050 Hz, 8-bit mono PCM; voice parameters include pitch, speed, mouth, throat, and optional phonetic input.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
