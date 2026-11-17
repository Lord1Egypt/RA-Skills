## Description:

Recognizes vehicle license documents and receipt or invoice images from URLs, local files, or selected OpenClaw session images and returns structured JSON data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leeee0923](https://clawhub.ai/user/leeee0923)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to send vehicle registration, receipt, or invoice images to a configured SmartOCR service and receive extracted fields as structured JSON. It also supports extracting recently uploaded images from OpenClaw session files when direct image access is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload local or session-derived images to a configured OCR endpoint.

Mitigation: Use it only for documents approved for transfer to the configured service, prefer the default HTTPS endpoint or a trusted HTTPS host, and use a limited API key.

Risk: The session helper reads OpenClaw session history and may select recent uploaded images without strong scoping or confirmation.

Mitigation: Avoid the session helper unless the target session and image can be verified, or pass an explicit session path and count after review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leeee0923/skills/smartocr)
- [Publisher profile](https://clawhub.ai/user/leeee0923)
- [SmartOCR service endpoint](https://smartocr.yunlizhi.cn)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON OCR results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, the requests package, SMARTOCR_API_KEY, and optionally SMARTOCR_API_URL or OPENCLAW_HOME.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
