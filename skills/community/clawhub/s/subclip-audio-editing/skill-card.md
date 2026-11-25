## Description:

Add and mix music, voiceover, sound effects, and existing audio assets through Subclip AudioPanel, AudioLayer, and UnifiedTimeline. Use for requests about audio, music, voice, volume, muting, fades, looping, pan, playback rate, silence removal, or voice enhancement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[prosamik](https://clawhub.ai/user/prosamik)

### License/Terms of Use:

MIT-0

## Use Case:

External video editors use this skill to add, arrange, and mix music, voiceover, sound effects, and other audio in a Subclip project. It guides audio import, timeline placement, transcription, and audio controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud transcription and authenticated AI audio workflows may use external services or consume credits.

Mitigation: Use cloud transcription when appropriate and obtain authorization before starting it; confirm before any route that consumes credits.

Risk: Audio from the source video can overlap with extracted narration and make the voice sound doubled.

Mitigation: When extracted narration is the master track, mute all video audio and check for competing voice tracks.

## Reference(s):

- [Subclip Audio Editing on ClawHub](https://clawhub.ai/prosamik/skills/subclip-audio-editing)

## Skill Output:

**Output Type(s):** [API Calls, Guidance]

**Output Format:** [Audio editing tool calls with concise natural-language guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
