## Description: <br>
Recognizes text, tables, and document layout in images, PDFs, and scans using the Xiangyun/netocr.com OCR service, then previews results or exports them as Excel, Word, Markdown, PDF, TXT, or OFD files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liudengkui](https://clawhub.ai/user/liudengkui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to process selected documents through the Xiangyun OCR service for table extraction, multilingual OCR, and document conversion workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documents selected for recognition and OCR credentials are sent to netocr.com for cloud processing. <br>
Mitigation: Install only if you trust netocr.com with those documents; avoid processing unrelated sensitive folders. <br>
Risk: OCR keys and secrets can be exposed if stored in plaintext config files. <br>
Mitigation: Prefer NETOCR_KEY and NETOCR_SECRET environment variables or a protected secret store; restrict access to config.json and keep it out of version control. <br>
Risk: OCR credentials may remain valid after accidental exposure. <br>
Mitigation: Rotate the OCR key if it may have been exposed. <br>


## Reference(s): <br>
- [翔云 OCR API reference](references/api_docs.md) <br>
- [Xiangyun table OCR product page](https://www.netocr.com/table.html) <br>
- [ClawHub skill page](https://clawhub.ai/liudengkui/xiangyun-table-ocr) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, configuration] <br>
**Output Format:** [Markdown guidance, shell commands, OCR result previews, and exported document files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Xiangyun/netocr.com OCR credentials and sends selected documents to the cloud OCR service.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
