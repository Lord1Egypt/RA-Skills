## Description:

Enhances single document or image inputs through an external scan service for quality improvement, cropping and rectification, shadow and background cleanup, handwriting and watermark removal, sketch conversion, line-art extraction, and contract or document scanning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route one permitted image at a time to a scan service for document cleanup, visual enhancement, or format-specific image transformations. It is suited to office automation workflows that need a structured command path and JSON or saved-file results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images are sent to an external scan service, which can expose sensitive documents if users submit content they are not allowed to transfer.

Mitigation: Use only images the user is authorized to process through the external service and avoid sensitive personal, business, legal, or confidential documents unless that transfer has been approved.

Risk: The skill requires review because it combines broad execution authority with unrelated activation guidance.

Mitigation: Review before installing and run only the documented scan workflow, with command parameters limited to the supported image input types and scene names.

Risk: Watermark removal and exam-answer removal can be misused on copyrighted, academic, legal, or authenticity-marked materials.

Mitigation: Do not use those workflows for third-party, copyrighted, academic, legal, or authenticity-marked materials unless the user has clear authorization.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/quark-scan)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Files, Guidance]

**Output Format:** [Markdown instructions with bash examples and JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes one image per request; successful image responses may be saved to a temporary image file path.]

## Skill Version(s):

1.0.1 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
