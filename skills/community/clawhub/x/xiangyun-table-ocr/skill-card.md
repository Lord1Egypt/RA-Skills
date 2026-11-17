## Description:

This agent sends images, PDFs, and scanned documents to Xiangyun NetOCR for OCR, table extraction, layout recognition, and optional exports to Excel, Word, Markdown, PDF, TXT, or OFD.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liudengkui](https://clawhub.ai/user/liudengkui)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to recognize text, tables, and document layout from local images, PDFs, and scans through the Xiangyun NetOCR cloud service. It can preview recognition results and export processed documents in common office and text formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documents and OCR credentials are sent to the NetOCR cloud service during recognition.

Mitigation: Use the skill only for documents approved for NetOCR processing, and avoid sending sensitive or regulated content unless the service is authorized for that data.

Risk: OCR credentials can be stored in plaintext config.json.

Mitigation: Prefer NETOCR_KEY and NETOCR_SECRET environment variables or a managed secret store, and keep config.json out of shared repositories and sync folders.

Risk: Recognition results and exports can persist sensitive document contents locally.

Mitigation: Review or delete .table_result.json files and exported documents after processing sensitive inputs.

## Reference(s):

- [Xiangyun OCR API Reference](references/api_docs.md)
- [Xiangyun NetOCR Table Recognition Product Page](https://www.netocr.com/table.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown status output, JSON recognition results, and exported document files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create .table_result.json files beside processed inputs and exported xls, docx, md, pdf, txt, or ofd files when requested.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
