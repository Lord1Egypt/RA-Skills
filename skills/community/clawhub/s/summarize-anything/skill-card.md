## Description:

Extract, transcribe, clean, segment, and analyze long-form content from URLs, local media files, existing transcripts, and pasted text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chengjl19](https://clawhub.ai/user/chengjl19)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, researchers, and knowledge workers use this skill to turn articles, social posts, videos, podcasts, local media, transcripts, and pasted text into cleaned text, rough speaker transcripts, and analytical insight memos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Runtime setup may install packages with sudo or package managers.

Mitigation: Review setup behavior before installation, preinstall ffmpeg where possible, and run the skill where sudo and package-manager access are controlled.

Risk: Runtime setup may fetch media, clone and build external transcription tooling, and download model files.

Mitigation: Use a container or restricted environment with controlled network access, or provision whisper.cpp and required models through a trusted path before use.

Risk: Transcription and rough speaker segmentation can be imprecise.

Mitigation: Treat cleaned transcripts and speaker labels as reviewable outputs, preserve uncertainty, and avoid presenting rough segmentation as precise diarization.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chengjl19/skills/summarize-anything)
- [Workflow](references/workflow.md)
- [Invocation Examples](references/invocation-examples.md)
- [Transcript Cleaning](references/transcript-cleaning.md)
- [Speaker Segmentation](references/speaker-segmentation.md)
- [Insight Quality](references/insight-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance]

**Output Format:** [Markdown responses with optional transcript and memo files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce raw transcript, cleaned transcript, rough speaker transcript, and insight memo artifacts in the workspace.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
