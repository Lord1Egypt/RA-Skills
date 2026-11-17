## Description:

Extracts Chinese and English text from screenshots and can format results as plain text, structured exam content, or question-answer pairs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tom859174-sketch](https://clawhub.ai/user/tom859174-sketch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to extract text from screenshot image files, especially Chinese medical exam question screenshots. It returns plain OCR text or structured question and answer data for downstream review or processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OCR accuracy may be poor outside Chinese and English screenshot content because the OCR language is fixed.

Mitigation: Use it for the intended Chinese and English screenshot scope and review extracted text before relying on it.

Risk: The tool reads the image path provided by the user and can write a JSON result to an optional output path.

Mitigation: Provide only image paths intended for OCR and choose output paths where writing the JSON result is acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tom859174-sketch/skills/screenshot-ocr-tool)

## Skill Output:

**Output Type(s):** [Text, JSON, Files]

**Output Format:** [JSON object with OCR status, original text, processed text, and optional structured data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports text, structured, and question_answer modes; OCR language is fixed to Simplified Chinese plus English, and CLI output can be printed or written to a JSON file.]

## Skill Version(s):

1.0.1 (source: server release metadata; changelog: v1.0.1 - Bump version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
