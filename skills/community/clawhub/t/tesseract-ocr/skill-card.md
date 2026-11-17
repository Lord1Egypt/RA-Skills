## Description:

Extract text from images using the Tesseract OCR command-line engine, with examples for multilingual OCR and output options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whalefell](https://clawhub.ai/user/whalefell)

### License/Terms of Use:


## Use Case:

Developers and other agent users use this skill to extract text from image files with the Tesseract CLI, including multilingual recognition workflows for Chinese, English, Japanese, and Korean.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Package-manager commands can add or change system packages.

Mitigation: Review the Tesseract and language-pack install commands before running them, especially commands that use sudo.

Risk: OCR output may be inaccurate for low-quality images or complex layouts.

Mitigation: Use clear source images, review extracted text before relying on it, and apply post-processing for tables or multi-column documents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/whalefell/skills/tesseract-ocr)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline shell commands and OCR text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the Tesseract system package and any needed language packs to be installed locally.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
