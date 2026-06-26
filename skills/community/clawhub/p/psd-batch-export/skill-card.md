## Description: <br>
Production PSD batch workflow for analyzing Photoshop text layers, mapping Excel/CSV data to editable layers, previewing, exporting editable PSD and PNG batches, validating results, checking fonts/OCR dependencies, and using built-in PSD templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luis1213899](https://clawhub.ai/user/luis1213899) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and operations teams use this skill to automate Photoshop template personalization from spreadsheet data, generate previews and batch exports, and review structured validation reports before production use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read PSDs, spreadsheets, fonts, and generated images and write batch outputs or reports that may contain customer, event, or design data. <br>
Mitigation: Run it only on intended local input folders, review output paths before export, and handle generated PSD, PNG, and report files according to the data sensitivity of the source material. <br>
Risk: Optional LLM-assisted behavior may send prompts or derived design context to a configured provider when credentials such as OPENAI_API_KEY are present. <br>
Mitigation: Use optional LLM mode only with approved providers and approved data; unset credentials or avoid LLM commands for confidential customer or event data. <br>
Risk: OCR verification reports may contain extracted text from generated outputs. <br>
Mitigation: Treat OCR reports as sensitive local files and retain, share, or delete them under the same handling rules as the generated PSD and PNG outputs. <br>
Risk: Optional font downloads and manually supplied font files can affect output rendering and licensing obligations. <br>
Mitigation: Download fonts only from trusted sources, verify font license terms before commercial use, and run diagnostics before production batches. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luis1213899/psd-batch-export) <br>
- [Runtime compatibility](references/runtime-compat.md) <br>
- [Built-in template catalog](references/templates.json) <br>
- [Font setup notes](fonts/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with shell commands, JSON reports, editable PSD outputs, PNG exports, preview folders, and optional OCR verification reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Primary commands can produce structured JSON reports and local output directories for PSD, PNG, preview, and verification artifacts.] <br>

## Skill Version(s): <br>
4.4.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
