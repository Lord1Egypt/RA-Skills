## Description:

Extract text from images using Tesseract.js (OCR). Supports multi-language recognition including Chinese and English, region recognition, character whitelist filtering, text orientation detection, and can run in a Node.js environment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to extract text from local or trusted remote images, including screenshots and scanned images, with language, region, whitelist, orientation, and output-format controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: npm dependency downloads may introduce unreviewed package or supply-chain changes.

Mitigation: Install only in environments where dependency downloads are allowed, and pin tesseract.js with a reviewed lockfile before operational use.

Risk: Remote image URLs can expose private content to untrusted hosts or fetch content from untrusted locations.

Mitigation: Prefer local image files for private or regulated data, and use remote URLs only when the host is trusted.

## Reference(s):

- [Tesseract.js API Reference](references/api.md)
- [Tesseract.js Official API Documentation](https://github.com/naptha/tesseract.js/blob/master/docs/api.md)
- [Tesseract.js Language List](https://github.com/naptha/tesseract.js/blob/master/docs/tesseract_lang_list.md)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell and JavaScript examples; OCR execution can return plain text, JSON, hOCR, or TSV.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports language selection, region selection, character whitelists, page segmentation modes, OCR engine modes, DPI overrides, and orientation detection.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
