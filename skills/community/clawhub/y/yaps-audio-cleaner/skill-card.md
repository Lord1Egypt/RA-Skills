## Description:

Reduce noise, hiss, and static in a speech recording with Yaps and save a separate clean file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yaps](https://clawhub.ai/user/yaps)

### License/Terms of Use:

MIT

## Use Case:

People and agents cleaning speech recordings use this skill to run Yaps locally, preserve the original audio, and deliver a separate denoised file with processing details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The packaged adapter can invoke Yaps functions beyond audio cleaning, including transcription, meeting, account, and app-launch operations.

Mitigation: Review each requested command and approve only actions relevant to the user's task before execution.

Risk: An operation may download a model, access local audio or account state, or overwrite an existing output.

Mitigation: Check inputs, output paths, model download size, and account-refresh requests; require explicit authorization before downloads or overwrites.

## Reference(s):

- [Yaps Audio Cleaner on ClawHub](https://clawhub.ai/yaps/skills/yaps-audio-cleaner)
- [Yaps runtime guide](references/runtime.md)
- [Download Yaps](https://yaps.ai/download)

## Skill Output:

**Output Type(s):** [Files, Text, Guidance]

**Output Format:** [Cleaned audio file and Markdown summary with file link and processing metrics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves the source recording and checks output duration, channels, and speech quality where possible.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
