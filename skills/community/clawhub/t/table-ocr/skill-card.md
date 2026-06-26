## Description: <br>
OCR and extract tables from scanned PDFs and images using MinerU, converting image-based table content into structured Markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzlzyca](https://clawhub.ai/user/mzlzyca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation builders use this skill to extract structured table content from scanned PDFs and image files. It is useful for digitizing printed reports, financial statements, screenshots, and other image-based documents that contain tables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Processed PDFs, images, or URLs may be sent to MinerU during extraction. <br>
Mitigation: Avoid confidential files or internal URLs unless MinerU is approved for that data and workflow. <br>
Risk: MINERU_TOKEN is an API credential required by the CLI. <br>
Mitigation: Treat MINERU_TOKEN like an API key, avoid logging it, and review where the CLI stores authentication before use. <br>


## Reference(s): <br>
- [Table Ocr on ClawHub](https://clawhub.ai/mzlzyca/table-ocr) <br>
- [MinerU Homepage](https://mineru.net) <br>
- [MinerU GitHub Repository](https://github.com/opendatalab/MinerU) <br>
- [MinerU Open API Go Package](https://github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api) <br>
- [MinerU Token Management](https://mineru.net/apiManage/token) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct mineru-open-api output to stdout or an output directory; progress and status messages go to stderr.] <br>

## Skill Version(s): <br>
0.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
