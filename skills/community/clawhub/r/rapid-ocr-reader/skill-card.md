## Description:

Extracts text from images using OCR, including screenshots, photos, and other image files with Chinese and English text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rendaixue-byte](https://clawhub.ai/user/rendaixue-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to extract readable text and line-level OCR metadata from screenshots, document photos, diagrams, receipts, and other images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs Python dependencies and may download OCR models on first run.

Mitigation: Install only where pip installs and first-run model downloads are acceptable; pin dependency versions and prefetch or verify OCR models for controlled deployments.

Risk: Very large or untrusted image files can create resource-use or processing risks.

Mitigation: Apply file size, image dimension, timeout, and memory limits before running OCR on untrusted images.

Risk: OCR output may be incomplete or inaccurate for low-quality, distorted, handwritten, or language-mismatched images.

Mitigation: Review OCR results before using them for decisions, and preserve confidence scores and source image context when accuracy matters.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rendaixue-byte/skills/rapid-ocr-reader)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [JSON object containing extracted text, per-line confidence scores, bounding boxes, line count, errors, and image metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [First run may download OCR models; output quality depends on image clarity, OCR model behavior, and available runtime resources.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
