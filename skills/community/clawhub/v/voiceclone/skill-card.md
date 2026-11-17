## Description:

Provides MiniMax API voice cloning and text-to-speech workflows, including optional write-back of cloned voice mappings for reuse.

This skill is ready for commercial/non-commercial use.

## Publisher:

[socketnet](https://clawhub.ai/user/socketnet)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to clone user-provided voice audio with MiniMax and synthesize speech from cloned or existing voices. It also helps retain display-name to voice-id mappings for later TTS reuse.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The write-back feature can persist unsanitized display names or voice identifiers into the skill instruction file.

Mitigation: Use trusted voice names and display names, review mapping changes before reuse, and prefer a version that validates or escapes mapping fields.

Risk: The registry path option can point outside the documented skill file scope.

Mitigation: Use trusted registry paths only, avoid overriding the default skill file path, and prefer a version that removes or restricts the registry path option.

Risk: The skill sends user audio and text to MiniMax using a MiniMax API key.

Mitigation: Run only with authorized audio and text, protect API keys in environment variables, and confirm third-party API use is acceptable for the data involved.

Risk: Dependencies are not pinned to exact versions.

Mitigation: Install in an isolated environment and prefer a release that pins dependencies for repeatable review.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/socketnet/skills/voiceclone)
- [MiniMax Upload Clone Audio API](https://api.minimax.io/v1/files/upload)
- [MiniMax Voice Clone API](https://api.minimax.io/v1/voice_clone)
- [MiniMax Text-to-Audio API](https://api.minimax.io/v1/t2a_v2)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, API calls, Files]

**Output Format:** [Markdown instructions with shell command examples; runtime output is synthesized audio files and cloned voice mapping entries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a MiniMax API key; clone audio is uploaded to MiniMax and synthesized audio is written to the requested output path.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
