## Description: <br>
Perform OCR on image files (jpg, png, bmp, gif, tiff) using the system's `tesseract` binary and return extracted plain text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaarl92](https://clawhub.ai/user/kaarl92) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to extract plain text from image files and PDFs through local Tesseract OCR, with an optional OCR.space example for API-based OCR. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional OCR.space helper can send local images or image URLs to an external OCR service. <br>
Mitigation: Use the local Tesseract script for private or regulated documents, and run the OCR.space helper only when external upload is acceptable. <br>
Risk: PDF processing creates temporary page images on disk during OCR. <br>
Mitigation: Process sensitive PDFs in a controlled environment and verify temporary files are removed after execution. <br>


## Reference(s): <br>
- [Reference Documentation for Ocr](references/api_reference.md) <br>
- [OCR.space API endpoint](https://api.ocr.space/parse/image) <br>
- [OCR.space OCR API documentation](https://ocr.space/ocrapi) <br>
- [ClawHub skill page](https://clawhub.ai/kaarl92/sm-ocr-scanner) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text OCR output, with Markdown usage guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local OCR uses Tesseract with English language data by default; PDF inputs are converted to temporary page images before OCR.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
