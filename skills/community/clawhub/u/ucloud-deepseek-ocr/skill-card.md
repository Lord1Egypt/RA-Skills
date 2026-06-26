## Description: <br>
OCR text recognition using DeepSeek-OCR model. Use when user asks for OCR, text recognition, image text extraction, screenshot recognition, or converting images to text/markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qianjunye](https://clawhub.ai/user/qianjunye) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to extract text, markdown, or structured content from local image files and screenshots through a configured DeepSeek-OCR-compatible API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image content is uploaded to the configured OCR API and may expose sensitive visual data. <br>
Mitigation: Process only images approved for that provider, avoid sensitive images unless the provider is approved for them, and confirm DEEPSEEK_OCR_API_URL before use. <br>
Risk: The script sources ~/.openclaw-env before execution. <br>
Mitigation: Use a trusted ~/.openclaw-env file and keep DEEPSEEK_OCR_API_KEY private. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qianjunye/ucloud-deepseek-ocr) <br>
- [Default OCR API endpoint](https://api.modelverse.cn/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration] <br>
**Output Format:** [Plain text, markdown, or JSON returned by the OCR API through shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, base64, DEEPSEEK_OCR_API_KEY, and a local image file; optional output format defaults to markdown.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
