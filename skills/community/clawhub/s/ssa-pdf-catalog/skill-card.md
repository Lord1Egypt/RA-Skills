## Description:

Extracts product information from PDF product catalogs and mold drawings to generate a structured knowledge base and optional Excel fill data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cjboy007](https://clawhub.ai/user/cjboy007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to batch-extract model numbers, package specifications, customer item names, and lengths from PDF product catalogs. It helps create Markdown product entries, structured JSON product data, and optional Excel SKU-to-model updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installation and local PDF/OCR tooling can affect the runtime environment.

Mitigation: Install in an isolated virtual environment and pin dependency versions where possible.

Risk: The optional Excel path can modify an existing workbook.

Mitigation: Pass only a workbook intended for modification, preferably a copy.

Risk: PDF filenames, extracted text, and generated Markdown may contain untrusted content.

Mitigation: Run the script only on trusted PDF folders and treat generated Markdown as extracted data, not trusted agent instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cjboy007/skills/ssa-pdf-catalog)
- [Docling documentation](https://ds4sd.github.io/docling/)
- [pdftotext manual](https://linux.die.net/man/1/pdftotext)
- [OpenPyXL documentation](https://openpyxl.readthedocs.io/)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with bash commands; generated artifacts include Markdown files, JSON data, and optional Excel workbook edits.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local output files and can modify a supplied Excel workbook when an excel_path is provided.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
