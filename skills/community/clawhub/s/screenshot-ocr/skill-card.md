## Description:

Recognizes text from screenshots or image files and can copy OCR results to the clipboard or save them as TXT.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sxliuyu](https://clawhub.ai/user/sxliuyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill to extract Chinese, English, and numeric text from screenshots or image files, including table-like image content. It is useful when an agent needs OCR text output that can be copied or saved for follow-up work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Clipboard OCR can process sensitive screenshots and leave image data in a predictable temporary file.

Mitigation: Prefer file-based OCR for sensitive material, avoid clipboard OCR on confidential screenshots, and patch the skill to use secure temporary files that are deleted after use.

Risk: The OCR helper invokes a shell path for macOS clipboard extraction.

Mitigation: Review the script before installation and prefer a patched version that avoids shell=True.

Risk: The skill depends on local system packages and Python packages.

Mitigation: Install Tesseract through a trusted package manager and install Python dependencies without administrator privileges where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sxliuyu/skills/screenshot-ocr)
- [Tesseract for Windows installation reference](https://github.com/UB-Mannheim/tesseract/wiki)

## Skill Output:

**Output Type(s):** [text, files, shell commands]

**Output Format:** [Plain text OCR output, optional TXT files, and command-line usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports clipboard image input, image file input, optional copy-to-clipboard, and optional save-to-file behavior.]

## Skill Version(s):

1.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
