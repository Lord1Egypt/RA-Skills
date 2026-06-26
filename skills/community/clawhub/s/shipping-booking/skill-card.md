## Description: <br>
Extracts structured JSON from shipping booking notes and shipping instructions in PDFs, images, scans, Word, Excel, and RTF files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucezhouzhou](https://clawhub.ai/user/brucezhouzhou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Logistics teams and external users use this skill to extract booking and shipping-instruction fields from uploaded transport documents into a structured JSON record for review or downstream entry. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded booking-document text or images are sent to the configured AI provider for extraction. <br>
Mitigation: Confirm the selected provider and API key before use, avoid unrelated or highly sensitive files, and follow the provider's data-handling terms. <br>
Risk: Document parsers process PDFs, Office files, images, and RTF content from user uploads. <br>
Mitigation: Use patched parser dependencies, prefer pinned versions, and scan files before processing in sensitive environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brucezhouzhou/shipping-booking) <br>
- [Booking Note Schema](references/schema.md) <br>
- [Anthropic API host](https://api.anthropic.com) <br>
- [OpenAI API host](https://api.openai.com) <br>
- [DeepSeek API endpoint](https://api.deepseek.com/v1) <br>
- [DashScope OpenAI-compatible endpoint](https://dashscope.aliyuncs.com/compatible-mode/v1) <br>
- [Moonshot API endpoint](https://api.moonshot.cn/v1) <br>
- [Zhipu GLM API endpoint](https://open.bigmodel.cn/api/paas/v4) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON in a Markdown code block, with optional low-confidence guidance text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a booking or shipping-instruction file and an Anthropic or OpenAI-compatible API key; document text or images may be sent to the configured AI provider.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
