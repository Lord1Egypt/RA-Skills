## Description:

OCR text recognition using DeepSeek-OCR model. Use when user asks for OCR, text recognition, image text extraction, screenshot recognition, or converting images to text/markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qianjunye](https://clawhub.ai/user/qianjunye)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to extract text from local image files, screenshots, and document or table images through DeepSeek-OCR. It supports markdown, plain text, JSON, and similar OCR output requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected images are uploaded to the configured remote OCR API and may contain sensitive documents, screenshots, IDs, invoices, secrets, or regulated data.

Mitigation: Use the skill only with an approved OCR provider and avoid sending sensitive or regulated images unless that provider and use case have been approved.

Risk: The OCR API endpoint is configurable, so requests and the API key could be sent to an unexpected endpoint.

Mitigation: Review DEEPSEEK_OCR_API_URL before use and keep DEEPSEEK_OCR_API_KEY narrowly scoped.

Risk: The script sources ~/.openclaw-env as executable shell code.

Mitigation: Review and control writes to ~/.openclaw-env before running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qianjunye/skills/ucloud-deepseek-ocr)
- [Default ModelVerse chat completions endpoint](https://api.modelverse.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands]

**Output Format:** [Markdown, plain text, or JSON OCR content emitted as terminal output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local image path, DEEPSEEK_OCR_API_KEY, curl, jq, and base64; the script configures a maximum response length of 8192 tokens.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
