## Description:

Local text-to-voice generation for OpenClaw workspaces using a canonical txt-to-mp3 pipeline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[betonimig](https://clawhub.ai/user/betonimig)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to convert prepared text files into MP3 voice output at a stable canonical path, with helpers for dependency checks, voice selection, chunking long text, and Telegram voice delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill presents itself as local while using node-edge-tts, which may send text to an external Edge TTS service.

Mitigation: Review text sensitivity before conversion and use a pinned local dependency or offline TTS engine when privacy, confidentiality, or reproducibility matters.

Risk: Voice generation depends on local Node.js, ffmpeg, and node-edge-tts availability.

Mitigation: Run the status command before generation and resolve missing dependencies using the printed install hints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/betonimig/skills/text-to-voice-local)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Files, Text]

**Output Format:** [Shell command guidance and generated MP3 files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes canonical output to tmp/voice-mode-latest.mp3 and records the latest output path in skills/text-to-voice-local/state/last-output.txt.]

## Skill Version(s):

1.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
