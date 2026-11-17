## Description:

Generate spectrograms and feature-panel visualizations from audio with the songsee CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate local spectrograms and multi-panel audio feature visualizations from audio files or stdin while preserving security guardrails for private audio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing and running an external Homebrew CLI from an upstream tap may not match every user's trust expectations.

Mitigation: Confirm acceptance of the disclosed steipete/tap/songsee Homebrew dependency before installation or use.

Risk: Generated visualizations and source audio can expose private content if transmitted over the network.

Mitigation: Keep songsee output local and do not pipe audio or visualization output to network-transmitting commands.

Risk: Spectrograms can reveal speech timing and patterns from sensitive recordings.

Mitigation: Confirm user intent before processing files whose names suggest therapy, medical, legal, meeting, voice memo, or other private content.

Risk: Extreme dimensions, many visualization panels, or long audio can consume substantial memory, disk, or processing resources.

Mitigation: Ask for confirmation before dimensions above 5000px, all panels simultaneously, or audio longer than 60 minutes.

Risk: Direct ffmpeg invocation expands the workflow beyond local audio visualization controls.

Mitigation: Let songsee handle non-native audio decoding internally rather than constructing direct ffmpeg commands.

## Reference(s):

- [Songsee upstream project](https://github.com/steipete/songsee)
- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/skills/songsee-hardened)
- [Faberlens songsee safety report](https://faberlens.ai/explore/songsee)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and local file-output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the local songsee CLI; Homebrew installation requires steipete/tap/songsee and the songsee binary.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
