## Description: <br>
Extract text from images using Tesseract.js (OCR). Supports multi-language recognition including Chinese and English, region recognition, character whitelist filtering, text orientation detection, and can run in a Node.js environment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to extract text from local images or trusted image URLs, including screenshots, scanned images, region-specific OCR, character-filtered OCR, and text orientation detection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote image URLs can expose image contents or retrieve untrusted remote resources. <br>
Mitigation: Use local files for sensitive images and pass only trusted image URLs. <br>
Risk: Installing the Node dependency downloads third-party code and may create or modify npm files in the skill directory. <br>
Mitigation: Install dependencies in a controlled environment and review dependency changes before deployment. <br>


## Reference(s): <br>
- [Tesseract.js Full API Reference](references/api.md) <br>
- [Tesseract.js Official API Documentation](https://github.com/naptha/tesseract.js/blob/master/docs/api.md) <br>
- [Tesseract.js Language List](https://github.com/naptha/tesseract.js/blob/master/docs/tesseract_lang_list.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text, JSON, hOCR, TSV, Markdown guidance, JavaScript snippets, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [OCR output depends on image quality, selected language data, page segmentation mode, OCR engine mode, optional region selection, character whitelist, and DPI settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
