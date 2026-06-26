## Description: <br>
Extracts product information from PDF product catalogs and mold drawings, then generates structured knowledge-base outputs and optional Excel fill data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cjboy007](https://clawhub.ai/user/cjboy007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to batch-process product catalog PDFs, extract model numbers, package specifications, customer item names, and lengths, and build product knowledge-base files. It also supports optional SKU-to-model Excel filling for catalog maintenance workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write generated files and optionally modify an Excel workbook in place. <br>
Mitigation: Use copies of PDFs and spreadsheets, choose a dedicated output directory, and avoid production workbooks unless in-place edits are intended. <br>
Risk: PDF text extraction and OCR may produce missing or incorrect product fields. <br>
Mitigation: Review the generated Markdown and JSON outputs, especially entries marked as missing, before relying on the extracted catalog data. <br>


## Reference(s): <br>
- [Docling documentation](https://ds4sd.github.io/docling/) <br>
- [pdftotext manual](https://linux.die.net/man/1/pdftotext) <br>
- [OpenPyXL documentation](https://openpyxl.readthedocs.io/) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, JSON, Excel workbook updates, shell commands, guidance] <br>
**Output Format:** [Markdown files, structured JSON, terminal status text, and optional in-place Excel workbook updates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes generated catalog files to the selected output directory and modifies the workbook passed with --excel-path when that option is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
