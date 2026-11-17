## Description:

Generates timed Chinese narration audio from a timestamped script using MiMo, Fish Audio, or a configured IndexTTS service, with optional experimental English-to-Chinese voice-cloned dubbing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[worldwonderer](https://clawhub.ai/user/worldwonderer)

### License/Terms of Use:

MIT

## Use Case:

Video editors and content creators use this skill to turn a timestamped narration script into Chinese speech segments aligned to a video timeline. An optional experimental mode translates and dubs English video using an authorized speaker's cloned voice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Narration text and, when cloning or dubbing, real voice audio are sent to the selected external provider.

Mitigation: Review media for sensitivity before use and choose a provider only when its data handling is acceptable.

Risk: Voice cloning may misuse a speaker's identity or rights.

Mitigation: Use cloning or dubbing only after confirming rights to the media and the speaker's consent.

Risk: Transcripts from third-party video in dub_brief.md may contain instructions that attempt to redirect the agent.

Mitigation: Treat transcript content as untrusted quoted media and limit the agent's dubbing step to producing dub_script.json.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/worldwonderer/skills/video-voiceover)
- [Self-hosted IndexTTS endpoint guide](artifact/references/index-tts.md)

## Skill Output:

**Output Type(s):** [Audio files, JSON metadata, Video file (experimental dub)]

**Output Format:** [WAV audio segments with JSON timing metadata; optional dubbed MP4]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Audio is aligned to supplied timestamps; experimental dubbing requires explicit voice-rights confirmation.]

## Skill Version(s):

1.0.8 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
