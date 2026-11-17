## Description:

A screen capture, OCR, and screen analysis skill for AI assistants that helps capture full-screen or regional screenshots, extract visible text, and inspect screen content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[datappt8](https://clawhub.ai/user/datappt8)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI assistants use this skill to capture intentional screen regions, run OCR on visible content, and perform basic screen analysis such as finding text, colors, or edges.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Screenshot and OCR workflows can capture passwords, messages, customer data, tokens, payment information, or other visible private content.

Mitigation: Run captures only for intentional tasks, prefer narrow regions over full-screen capture, store outputs in a location you can clean up, and delete screenshots and OCR text when no longer needed.

Risk: The optional Windows Tesseract installer downloads and silently runs an executable without pinned checksum or signature verification.

Mitigation: Prefer manual installation from a trusted Tesseract source, or add checksum and signature verification before running the installer.

Risk: The packaging workflow can include generated captures, OCR text, logs, environment files, keys, or other private files if run from a directory containing them.

Mitigation: Package from a clean release directory and inspect the archive contents before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/datappt8/skills/screen-capture-hub)
- [Usage examples](references/usage_examples.md)
- [Tesseract OCR setup guide](docs/OCR_SETUP_GUIDE.md)
- [Tesseract OCR project](https://github.com/tesseract-ocr/tesseract)
- [Tesseract documentation](https://tesseract-ocr.github.io/)
- [UB Mannheim Tesseract installer](https://github.com/UB-Mannheim/tesseract/wiki)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with inline shell commands; generated artifacts may include PNG screenshots, TXT OCR output, or JSON analysis files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Screen captures and OCR output can contain sensitive visible information and should be intentionally scoped and deleted when no longer needed.]

## Skill Version(s):

1.0.0 (source: evidence.json release metadata, SKILL.md frontmatter, package.json, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
