## Description:

Short Video Content Replicator is an OpenClaw skill that orchestrates a six-step workflow for Douyin, Bilibili, or local short-video inputs, producing separated vocals, transcription text, corrected text, and punctuated final text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangminrui2022](https://clawhub.ai/user/wangminrui2022)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to process short-video URLs or local media folders into local audio and text artifacts for content adaptation, transcription, and TTS training preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow downloads online video and writes local media and text artifacts.

Mitigation: Run it only for content you are permitted to process and direct outputs to a non-sensitive directory.

Risk: The workflow depends on other local skills and scripts.

Mitigation: Review and install the required sibling skills before execution, and run it from the expected skills layout.

Risk: The transcription flow is Chinese-first and generated text may be imperfect.

Mitigation: Review transcripts and corrected text before reuse, publication, or downstream training.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangminrui2022/skills/short-video-content-replicator)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with shell commands and local file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes video, MP3, vocals, transcript, corrected text, and final text outputs under the configured output root.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
