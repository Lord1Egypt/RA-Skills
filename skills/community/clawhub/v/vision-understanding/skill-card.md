## Description:

Turn images, video, audio, or documents into text for captioning, tagging, transcription, summarization, OCR, visual question answering, and structured extraction from media.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runware](https://clawhub.ai/user/runware)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to route media inputs to suitable multimodal models and request grounded text outputs such as captions, tags, transcripts, summaries, answers, or structured extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Media inputs may be disclosed to external model providers during processing.

Mitigation: Do not use the skill with highly sensitive IDs, medical records, financial documents, private recordings, or confidential screenshots unless that disclosure is acceptable.

Risk: Multimodal model outputs may include unreadable, absent, or invented details.

Mitigation: Ask the model to stay grounded in visible or audible content, report uncertainty, and validate that the output matches the requested fields or format.

## Reference(s):

- [Vision Understanding skill page](https://clawhub.ai/runware/skills/vision-understanding)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code, commands, and structured output instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides agents to validate that media outputs match the requested shape and remain grounded in visible or audible content.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
