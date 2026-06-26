## Description: <br>
用于识别图片和 PDF 文档，调用你已配置的 OCR 与多模态服务输出 Markdown 结果，并可按需发送到飞书。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangxusong637](https://clawhub.ai/user/zhangxusong637) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to extract structured Markdown from images, screenshots, scanned documents, receipts, tables, and PDFs. It can return local Markdown results and, when explicitly enabled, send recognition output to Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Images, PDFs, and extracted text can be sent to configured OCR and multimodal providers. <br>
Mitigation: Use trusted provider endpoints and avoid processing sensitive documents unless the data-sharing path is approved. <br>
Risk: Remote attachment input can forward authorization or cookie headers to download hosts. <br>
Mitigation: Keep remote input disabled by default and provide attachment credentials only for trusted hosts. <br>
Risk: Recognition results can be sent to Feishu when auto-send is explicitly enabled. <br>
Mitigation: Keep Feishu sending disabled for sensitive documents or require explicit confirmation and a verified recipient. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangxusong637/vision-ocr) <br>
- [README.md](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text, Markdown result files, and concise chat replies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [OCR-only mode can return raw OCR text; PDF mode can process pages separately; Feishu sending and remote input require explicit enablement.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata, package.json, skill.json, README.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
