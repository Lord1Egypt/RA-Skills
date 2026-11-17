## Description:

Text-to-speech conversion using the GLM-TTS service via the `uvx zai-tts` command for generating audio from text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[al-one](https://clawhub.ai/user/al-one)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to convert supplied text or text files into WAV speech output with selectable GLM-TTS voices, speed, and volume.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to provide a browser-derived Z.ai session token to a command-line package.

Mitigation: Use only when comfortable sharing that token with the client, protect the token as a secret, and prefer a proper scoped API credential if one is available.

Risk: The command uses an unpinned runtime package.

Mitigation: Prefer a version-pinned client or review the package version before installing and executing it.

Risk: Selected text or files are sent to an external TTS service.

Mitigation: Avoid processing sensitive documents, private prompts, or regulated data unless the service and account terms are approved for that use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/al-one/skills/zai-tts)
- [Zai-TTS homepage](https://github.com/aahl/zai-tts)
- [Z.ai audio service](https://audio.z.ai)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Audio]

**Output Format:** [Markdown guidance with inline shell commands; generated command outputs WAV audio files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires `uvx`, `ZAI_AUDIO_USERID`, and `ZAI_AUDIO_TOKEN`; supports text input, file input, voice selection, speed, and volume options.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
