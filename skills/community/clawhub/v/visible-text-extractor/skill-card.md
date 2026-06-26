## Description: <br>
Extract and reconstruct as much visible text as possible from webpage URLs, article pages, screenshots, long images, image directories, and GIFs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wunianze666-netizen](https://clawhub.ai/user/wunianze666-netizen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and content operations teams use this skill to recover readable text from web articles, WeChat posts, screenshots, long images, GIFs, and image folders when normal copy and paste is incomplete. It emphasizes clean markdown and Word deliverables while preserving raw OCR or JSON audit layers when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can fetch arbitrary web content and process private pages or sensitive documents. <br>
Mitigation: Use it only with URLs and files the operator is authorized to process, and isolate internal or credentialed sources before running extraction. <br>
Risk: Generated documents can optionally be sent to Feishu. <br>
Mitigation: Use the send option only when external transfer is explicitly intended, and review the generated DOCX before sharing. <br>
Risk: OCR and browser extraction can be incomplete, blocked, or noisy. <br>
Mitigation: Keep raw JSON or OCR audit output when accuracy matters, mark uncertainty clearly, and compare important results against the original source. <br>


## Reference(s): <br>
- [Visible Text Extractor on ClawHub](https://clawhub.ai/wunianze666-netizen/visible-text-extractor) <br>
- [Publisher profile](https://clawhub.ai/user/wunianze666-netizen) <br>
- [Usage guide](USAGE.md) <br>
- [Output schema](references/output-schema.md) <br>
- [Deliverable workflow](references/deliverable-workflow.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [Universal article extractor spec](references/universal-article-extractor-spec.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, DOCX, shell commands, guidance] <br>
**Output Format:** [Markdown, JSON, DOCX files, and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can preserve raw OCR candidates and uncertainty notes alongside cleaned reader-facing output.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
