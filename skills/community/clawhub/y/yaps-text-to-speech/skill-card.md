## Description:

Turn text into spoken audio with Yaps by choosing a supported voice and language and saving the result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yaps](https://clawhub.ai/user/yaps)

### License/Terms of Use:

MIT

## Use Case:

People using an agent on a computer with Yaps installed can generate and save spoken audio from supplied text, selecting a supported voice and language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled Yaps integration can expose transcription, subtitles, meetings, and other workflows beyond text-to-speech.

Mitigation: Review requested actions and authorize only the Yaps commands needed for the intended task.

Risk: Invoking Yaps may check account readiness or process local audio and video files.

Mitigation: Confirm account checks and file access before allowing the agent to run them.

## Reference(s):

- [Yaps runtime guide](references/runtime.md)
- [Yaps skill release](https://clawhub.ai/yaps/skills/yaps-text-to-speech)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Text with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Directs Yaps to save a local WAV file; check that the audio is complete and playable.]

## Skill Version(s):

1.0.2 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
