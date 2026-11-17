## Description: <br>
使用 Z.ai GLM-4.1V-thinking-flash 模型进行图片理解和分析，支持图片内容描述、视觉问答、文字和结构化信息提取、场景分析以及本地图片转 Base64 后调用远程 API 返回结构化分析结果。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[internettrollwatt](https://clawhub.ai/user/internettrollwatt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to send a user-provided image and prompt to Z.ai's GLM-4.1V-thinking-flash vision API, then return image descriptions, OCR-style extraction, visual question answering, chart or document analysis, and structured summaries. It is useful when an agent needs visual understanding rather than image transformation or file conversion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends selected images, prompts, and model responses to Z.ai/Open BigModel for remote analysis. <br>
Mitigation: Use it only when the user has permission to process the image with that provider, and avoid IDs, medical records, confidential screenshots, or private documents unless the provider terms and data handling are acceptable. <br>
Risk: Raw responses and reasoning output can include sensitive image-derived details. <br>
Mitigation: Avoid saving full raw responses or reasoning output unless needed, and redact sensitive details before sharing logs or artifacts. <br>
Risk: Vision model analysis can be incomplete or incorrect for OCR, charts, documents, or ambiguous images. <br>
Mitigation: Treat extracted text, numbers, and conclusions as assistive output and verify important results against the source image before acting on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/internettrollwatt/skills/zai-image-understanding) <br>
- [Z.ai GLM-4.1V-thinking-flash API specification](references/api-spec.md) <br>
- [Prompt guide](references/prompt-guide.md) <br>
- [Z.ai API error codes](references/error-codes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [JSON response containing success status, analysis text, optional reasoning content, raw API response metadata, usage, timing, and error fields; the agent may summarize it as Markdown or plain text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a ZAI_API_KEY credential and network access to open.bigmodel.cn; supports one image per request, HTTP/HTTPS image URLs, and local images converted to Base64 data URLs.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
