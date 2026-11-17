## Description:

Transforms pasted transcript text into structured internal training outlines and supports lesson-by-lesson expansion into detailed Chinese training documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0x00pluto](https://clawhub.ai/user/0x00pluto)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and training-content authors use this skill to convert pasted training transcripts into internal course outlines, lesson-level documents, and compiled long-form training materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Training transcripts may contain confidential business details, personal data, customer information, secrets, or regulated content.

Mitigation: Redact sensitive material before use unless the user is authorized to process that content.

Risk: The generated training material may overstate or add facts that are not present in the source transcript.

Mitigation: Require source evidence for each lesson and mark missing information as needing supplementation.

Risk: The skill defaults to Chinese-language document structure, which may not match every deployment context.

Mitigation: Confirm the desired language and document conventions before producing final training materials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0x00pluto/skills/training-content-extractor)
- [Skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Chinese Markdown training outlines, lesson documents, and compiled training documents]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Segmented output by default to avoid excessively long responses.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
