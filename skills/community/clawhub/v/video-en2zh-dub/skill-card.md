## Description:

Turns spoken English videos into Chinese-dubbed videos using transcription, subtitle translation, speech synthesis, and video assembly, with an optional bilingual audio track.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anshanzhaoqian](https://clawhub.ai/user/anshanzhaoqian)

### License/Terms of Use:

MIT-0

## Use Case:

Video creators and editors use this skill to make Chinese-dubbed versions of spoken English videos, either replacing the original audio or retaining it as a selectable track.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Translated subtitle text may be sent to Microsoft's online edge-tts service, exposing confidential speech content.

Mitigation: Review video sensitivity before use and avoid the online speech-synthesis stage for confidential content.

Risk: Installing unpinned dependencies may limit supply-chain reproducibility.

Mitigation: Run in an isolated environment and pin dependencies before installation.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/anshanzhaoqian/skills/video-en2zh-dub)
- [Troubleshooting notes](references/pitfalls.md)
- [Audio synchronization guidance](references/sync-tuning.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown instructions with shell commands and translated SRT subtitles]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Following the workflow creates Chinese subtitles, an MP3 voice track, and a dubbed MP4; optional bilingual audio is supported.]

## Skill Version(s):

1.0.2 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
