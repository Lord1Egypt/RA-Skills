## Description:

Analyze local or linked video files and convert them into structured summaries of features, functions, workflows, or topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrgoodgreen](https://clawhub.ai/user/mrgoodgreen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and analysts use this skill to process long or noisy videos into tracked transcripts and structured summaries. It is suited for walkthroughs, demo reviews, feature extraction, timestamped summaries, and cases where media access or long-running transcription needs explicit progress files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local video, audio, transcript, and progress content may be written under tmp/video_analysis/.

Mitigation: Run the skill in a dedicated private working directory and avoid shared or untrusted folders.

Risk: Automatic transcription and summarization can be noisy or incomplete, especially for long or poor-quality videos.

Mitigation: Review generated transcripts and final summaries before relying on them, and keep confidence caveats when source audio is uncertain.

Risk: Dependency and model changes can affect reproducibility.

Mitigation: Prefer pinned dependencies and model artifacts when stronger reproducibility is required.

## Reference(s):

- [Tracked Video Analysis Pipeline](references/pipeline.md)
- [ClawHub Skill Page](https://clawhub.ai/mrgoodgreen/skills/tracked-video-analysis)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown summaries with progress/status JSON files and transcript JSONL artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces tracked extraction and final structuring files under tmp/video_analysis/ when used as documented.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
