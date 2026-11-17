## Description:

Super OCR extracts text from images using intelligent engine selection across Tesseract, PaddleOCR, and macOS Vision for mixed-language documents and confidence-aware OCR results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nimachu](https://clawhub.ai/user/nimachu)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users use Super OCR to extract text from single images or batches, especially mixed-language and complex documents, with engine selection, confidence scores, and optional JSON output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Environment-modifying dependency installation can install or change OCR packages during setup.

Mitigation: Review the setup path before installation, use a virtual environment, avoid elevated privileges, and manually pin and review OCR dependencies.

Risk: Tesseract preprocessing uses predictable temporary filenames beside the input image.

Mitigation: Run OCR in a private working directory and avoid shared directories where a matching *_tess_processed.png file may already exist.

## Reference(s):

- [API Reference](references/api-reference.md)
- [Engine Comparison](references/engine-comparison.md)
- [Troubleshooting](references/troubleshooting.md)
- [Tesseract Windows Installation Wiki](https://github.com/UB-Mannheim/tesseract/wiki)

## Skill Output:

**Output Type(s):** [text, json, files, guidance]

**Output Format:** [Plain text, structured text, or JSON OCR results with extracted text, confidence, engine, timing, and optional line metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write per-image *_ocr.json files when an output directory is provided; verbose mode includes timing, confidence, and engine details.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
