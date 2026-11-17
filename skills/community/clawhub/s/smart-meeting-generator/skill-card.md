## Description:

Converts PDF or Word meeting transcripts into structured, detailed meeting minutes using a multi-pass extraction, validation, supplementation, and final review workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crayfish153](https://clawhub.ai/user/crayfish153)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and external teams use this skill to turn raw meeting transcripts into formal meeting minutes with discussion topics, participants, decisions, and action items. It is intended for detailed meeting-record cleanup rather than terse summarization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full meeting transcripts may contain confidential, regulated, personal, legal, financial, or internal information before they are sent for DeepSeek processing.

Mitigation: Use only with organizational approval for DeepSeek processing, and redact or avoid sensitive transcripts unless that processing path is approved.

Risk: Auxiliary packaging and verification utilities are flagged for unsafe archive handling.

Mitigation: Treat included scripts as developer utilities only, and avoid verifying untrusted .skill archives or packaging directories that may contain secrets until the archive extraction and file inclusion logic is fixed.

Risk: The artifact asks for exhaustive coverage and a minimum output length, which can encourage overly long notes if source material is sparse.

Mitigation: Review generated minutes against the source transcript before use, especially when the transcript is short or incomplete.

## Reference(s):

- [AI Prompt Templates](artifact/references/ai-prompts.md)
- [Output Format Specifications](artifact/references/format-specs.md)
- [ClawHub Skill Page](https://clawhub.ai/crayfish153/skills/smart-meeting-generator)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured meeting minutes, with optional PDF or Word formatting guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Targets a minimum length of 2000 words or characters and may include validation summaries when the full workflow is used.]

## Skill Version(s):

1.0.0 (source: frontmatter, _meta.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
