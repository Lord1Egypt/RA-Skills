## Description:

Extract text from images and scanned documents using PaddleOCR - supports 100+ languages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duykhangdangzn1](https://clawhub.ai/user/duykhangdangzn1)

### License/Terms of Use:


## Use Case:

Developers, analysts, and agents use this skill to extract readable text, bounding boxes, and confidence data from images, screenshots, scanned PDFs, receipts, business cards, and multilingual documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OCR inputs may contain sensitive IDs, receipts, or business documents, and extracted text may expose that information to the agent workflow.

Mitigation: Run OCR only on documents the user is comfortable processing, and avoid sensitive documents unless the handling path is approved.

Risk: Installing OCR dependencies directly into a shared environment can affect other projects or inherit unpinned package changes.

Mitigation: Install the skill dependencies in a dedicated virtual environment or container and pin dependency versions where practical.

Risk: The artifact includes sample URL image fetching, which can retrieve untrusted remote content.

Mitigation: Only fetch images from explicitly trusted URLs and adapt production code to validate sources before OCR processing.

Risk: Sample PDF conversion writes temporary page images during OCR processing.

Mitigation: Use secure temporary files and ensure cleanup after processing.

## Reference(s):

- [PaddleOCR GitHub](https://github.com/PaddlePaddle/PaddleOCR)
- [PaddleOCR Model Zoo](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.7/doc/doc_en/models_list_en.md)
- [PaddleOCR Multi-language Support](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.7/doc/doc_en/multi_languages_en.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell code blocks; OCR runs produce extracted text plus position and confidence data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include bounding boxes, confidence scores, language codes, reconstructed layout, and batch-processing examples.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
