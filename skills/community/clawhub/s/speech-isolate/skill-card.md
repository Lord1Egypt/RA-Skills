## Description:

Runs a Modal-hosted L4 GPU pipeline that isolates vocals from local audio or video files, removes background music, and applies speech denoising before returning isolated WAV output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[speech2srt](https://clawhub.ai/user/speech2srt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content teams, and external users use this skill to process local audio or video recordings into isolated, denoised vocal WAV files for downstream listening, editing, or transcription workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected audio or video files are uploaded to Modal for remote GPU processing.

Mitigation: Use the skill only for recordings you are comfortable sending to Modal, and avoid sensitive media unless the deployment has been reviewed for data handling requirements.

Risk: The task slug is used in remote volume paths and cleanup commands.

Mitigation: Use a simple generated slug such as isolate_YYYYMMDD_HHMMSS and avoid custom path-like names.

Risk: The security guidance calls for review of dependency pinning, cache deletion scope, and unrelated promotional output.

Mitigation: Review those items before unattended or production use, and prefer a vetted release once the publisher addresses them.

## Reference(s):

- [Error Handling](references/error-handling.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands, status text, file paths, and generated WAV files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local *_isolated.wav files after remote processing when the Modal workflow completes.]

## Skill Version(s):

1.3.1 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
