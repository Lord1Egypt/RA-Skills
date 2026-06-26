## Description: <br>
Recognizes vehicle registration documents and receipts or invoices from image URLs, local image files, or recent OpenClaw session images, returning structured JSON through the SmartOCR API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leeee0923](https://clawhub.ai/user/leeee0923) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to extract structured fields from vehicle registration pages, receipts, and invoices supplied as image URLs, local files, or recent conversation uploads. It is useful when an agent needs machine-readable OCR output from supported document images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Vehicle documents, receipts, invoices, and recent chat-uploaded images may contain sensitive information and are uploaded to the configured SmartOCR API. <br>
Mitigation: Use the skill only with a trusted SmartOCR endpoint, confirm the intended image before processing, and prefer explicit file paths unless session-image extraction is necessary. <br>
Risk: The session helper may process the most recent OpenClaw session image rather than the document the user intended. <br>
Mitigation: Use the --session, --agent, or --count options deliberately and verify that the selected session image is appropriate before sending it for OCR. <br>
Risk: The skill requires an API key for SmartOCR access. <br>
Mitigation: Store SMARTOCR_API_KEY in OpenClaw environment configuration and avoid placing the key in prompts, command history examples, or shared files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leeee0923/smartocr) <br>
- [Publisher profile](https://clawhub.ai/user/leeee0923) <br>
- [SmartOCR API endpoint](https://smartocr.yunlizhi.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Structured JSON or pretty-printed JSON text emitted by command-line scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SMARTOCR_API_KEY and optionally SMARTOCR_API_URL; local files and session images are uploaded to the configured SmartOCR endpoint.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
