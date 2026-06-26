## Description: <br>
Generates, decodes, styles, and batch-processes QR codes and common barcode formats with Python scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaiyuelv](https://clawhub.ai/user/kaiyuelv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical users use this skill to create QR codes for text, URLs, WiFi credentials, contact cards, and common barcode formats, then decode or restyle those images locally. It also supports batch workflows from CSV or JSON data sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Batch generation may write files outside the selected output directory when input CSV or JSON filename fields contain unsafe paths. <br>
Mitigation: Use only trusted batch files, inspect or sanitize filename fields before execution, and run the scripts in an isolated working directory. <br>
Risk: WiFi credentials, contact details, and decoded payloads can be sensitive when stored as generated QR images or JSON reports. <br>
Mitigation: Store generated images and decode reports in controlled locations, limit sharing, and remove sensitive outputs when no longer needed. <br>
Risk: Unreviewed dependency versions or local image-processing libraries may introduce operational or security issues. <br>
Mitigation: Install the toolkit in an isolated Python environment and pin or review dependencies before use. <br>


## Reference(s): <br>
- [QR Code Standards](artifact/references/qr-standards.md) <br>
- [Barcode Types Reference](artifact/references/barcode-types.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/kaiyuelv/qr-barcode-toolkit) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration, Files] <br>
**Output Format:** [Markdown guidance with shell command examples; scripts produce PNG images and optional JSON decode reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local scripts can write image files and batch outputs based on user-supplied paths and CSV or JSON input.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
