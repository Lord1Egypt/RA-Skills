## Description: <br>
A lightweight file parsing skill that sends supported images or PDFs to WPS/Kingsoft OCR services and returns extracted text, handwriting, formulas, tables, documents, and seals as Markdown-oriented output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[randyliu111](https://clawhub.ai/user/randyliu111) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to extract text from user-provided document scans, screenshots, photos, invoices, business cards, and other supported files before editing, translating, or summarizing the content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided files or URLs are sent to WPS/Kingsoft cloud services for OCR processing. <br>
Mitigation: Use the skill only when the user is comfortable sharing the exact input with aiwrite.wps.cn, especially for IDs, contracts, invoices, screenshots, and private links. <br>
Risk: The skill requires a WPS_OCR_ACCESS_KEY and documentation suggests storing it in an environment file. <br>
Mitigation: Use a dedicated key, restrict access to any environment file that stores it, and rotate the key if it may have been exposed. <br>


## Reference(s): <br>
- [WPS OCR access key](https://aiwrite.wps.cn/pdf/parse/accesskey/) <br>
- [WPS OCR demo platform](https://aiwrite.wps.cn/pdf/parse/web/) <br>
- [ClawHub skill page](https://clawhub.ai/randyliu111/wps-ocr) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON] <br>
**Output Format:** [JSON containing status fields and a markdown_text value with recognized OCR content.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns API or validation errors when credentials, input type, file size, URL validation, network access, or OCR recognition fails.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
