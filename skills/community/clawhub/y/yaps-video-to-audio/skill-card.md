## Description:

Save audio from a video as MP3, WAV, or M4A using Yaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yaps](https://clawhub.ai/user/yaps)

### License/Terms of Use:

MIT

## Use Case:

People using a local Yaps installation can extract a video's audio into a separate MP3, WAV, or M4A file while keeping the original video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled adapter can run Yaps features beyond extracting audio.

Mitigation: Review requested commands and allow only the audio extraction needed for the user's task.

Risk: Local account checks may discover or launch the Yaps app to refresh account status.

Mitigation: Use only on a trusted local machine and review account-related actions before running the skill.

## Reference(s):

- [Yaps runtime guide](references/runtime.md)
- [Yaps download](https://yaps.ai/download)
- [Yaps Video to Audio on ClawHub](https://clawhub.ai/yaps/skills/yaps-video-to-audio)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [MP3, WAV, or M4A audio file with concise status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves the source video and existing exports; checks that the new audio file is usable.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
