## Description: <br>
Extract text from images using the Tesseract OCR engine directly via command line. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[WhaleFell](https://clawhub.ai/user/WhaleFell) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, engineers, and other users can use this skill to extract text from image files, recognize multilingual image content, and run OCR tasks through the local Tesseract CLI without Python dependencies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing OCR tooling or language packs from untrusted sources can introduce supply-chain risk. <br>
Mitigation: Install Tesseract and language packs only from trusted package managers or verified upstream sources. <br>
Risk: OCR commands may process unintended local files or write results to an unexpected output path. <br>
Mitigation: Run OCR only on files the user intends to process and review output paths before saving results. <br>
Risk: OCR accuracy can be poor on low-quality images or complex layouts, producing incorrect extracted text. <br>
Mitigation: Use clear source images and review OCR output before relying on it, especially for tables, multi-column documents, or multilingual content. <br>
Risk: Requested languages may fail or produce incomplete output when the corresponding Tesseract language packs are not installed. <br>
Mitigation: Install the required language packs, such as chi_sim for Simplified Chinese, before running multilingual OCR commands. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and OCR command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on the installed Tesseract binary, selected language packs, image quality, and requested output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
