## Description: <br>
Extracts content from DOCX, XLSX, PDF, and image files and converts the extracted text and tables into Markdown, with OCR support for scanned PDFs and images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sinoslug](https://clawhub.ai/user/sinoslug) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document reviewers use this skill to read existing Word, Excel, PDF, and image documents and convert their contents into Markdown without creating or editing the source files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OCR can expose document images or extracted text to the configured MCP OCR service, depending on that service's privacy and retention behavior. <br>
Mitigation: Use OCR only for files appropriate for that service, and avoid confidential scans or images unless the service's privacy and retention terms are acceptable. <br>
Risk: Scanned PDF processing can create temporary page images under /tmp that may persist after extraction. <br>
Mitigation: Check and clean temporary PDF page images after processing sensitive PDFs. <br>
Risk: The workflow may require installing Python packages before document extraction. <br>
Mitigation: Install only the documented packages from trusted sources in an environment where those dependencies are acceptable. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with extracted text, metadata, and tables; may include shell commands for required Python packages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only extraction workflow; OCR depends on the configured MCP OCR tool.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
