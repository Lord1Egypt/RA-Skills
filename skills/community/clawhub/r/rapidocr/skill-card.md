## Description:

Extract text from local image files with RapidOCR. Use when the user wants OCR on a JPG, PNG, WEBP, BMP, or TIFF image and may want plain text or JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidai](https://clawhub.ai/user/rapidai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run local OCR on supported image files and receive recognized text as plain text or structured JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OCR may process sensitive information contained in local image files.

Mitigation: Avoid running OCR on sensitive images unless the local RapidOCR and onnxruntime installation is approved for that content.

Risk: Installing Python OCR dependencies from an untrusted package index can introduce runtime supply-chain risk.

Mitigation: Install rapidocr and onnxruntime only from trusted package indexes or pinned requirements.

## Reference(s):

- [RapidOCR Documentation](https://rapidai.github.io/RapidOCRDocs)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Plain text or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [JSON mode includes text, lines, boxes, scores, and source.]

## Skill Version(s):

1.0.3 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
