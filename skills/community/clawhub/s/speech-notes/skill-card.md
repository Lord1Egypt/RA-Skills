## Description:

Speech Notes turns Chinese audio recordings or existing transcripts into structured speech or meeting notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guoqunabc](https://clawhub.ai/user/guoqunabc)

### License/Terms of Use:


## Use Case:

External users and teams use this skill to transcribe Chinese speech from recordings or existing transcripts and turn it into polished, structured notes for meetings, talks, and internal sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audio recordings and transcripts may contain sensitive speech content and may be processed through Feishu, Gemini, or Qwen depending on the available inputs.

Mitigation: Confirm that the selected transcription provider is acceptable for the content before processing and avoid submitting restricted or confidential recordings to unsupported services.

Risk: Original transcripts may be saved locally for review.

Mitigation: Keep local transcript files only in the intended workspace, limit retained content to what is needed for review, and remove local copies when they are no longer required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guoqunabc/skills/speech-notes)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown notes with supporting text, shell commands, and code snippets when transcription is required]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save original transcripts locally for review and may use Feishu STT, Gemini, or Qwen depending on available inputs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
