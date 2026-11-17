## Description:

Make a speaker-labeled meeting transcript in Yaps, correct and export it, and answer questions about it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yaps](https://clawhub.ai/user/yaps)

### License/Terms of Use:

MIT

## Use Case:

People with a local Yaps installation use this skill to transcribe meeting media, review and correct speaker labels, export transcripts, create recaps, and ask meeting-grounded questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Yaps access could affect meeting data beyond the requested task.

Mitigation: Limit commands to the selected meeting, keep cross-meeting searches opt-in, and preserve existing projects and exports.

Risk: Model or dependency downloads may be initiated during transcription.

Mitigation: Review download prompts and authorize the reported size before proceeding.

## Reference(s):

- [Yaps Meeting Transcription on ClawHub](https://clawhub.ai/yaps/skills/yaps-meeting-transcription)
- [Yaps download](https://yaps.ai/download)
- [Local runtime guide](artifact/references/runtime.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Speaker-labeled transcript and answers in text; optional Markdown exports and recaps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Meeting answers preserve source citations; recaps are interpretations rather than verbatim transcripts.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
