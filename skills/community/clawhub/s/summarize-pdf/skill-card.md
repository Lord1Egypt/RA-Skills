## Description: <br>
PDF to Markdown converter - extract text, tables and formulas from PDF files to clean Markdown. Use when converting PDF documents, extracting PDF content, parsing PDF text, or summarizing PDF reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tanis90](https://clawhub.ai/user/tanis90) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to convert local or URL-based PDF documents into Markdown for reading, extraction, parsing, analysis, or summarization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDFs are sent to MinerU's remote API for processing. <br>
Mitigation: Use only with documents that are acceptable for external processing; avoid confidential or regulated documents unless that data flow is approved. <br>
Risk: Installing the wrong CLI package could expose users to an untrusted implementation. <br>
Mitigation: Install the MinerU Open API CLI only from the expected MinerU/OpenDataLab sources listed by the release metadata. <br>


## Reference(s): <br>
- [Summarize Pdf on ClawHub](https://clawhub.ai/tanis90/summarize-pdf) <br>
- [MinerU](https://mineru.net) <br>
- [MinerU Open Source Project](https://github.com/opendatalab/MinerU) <br>
- [MinerU CLI](https://mineru.net/ecosystem?tab=cli) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses MinerU Open API flash extraction; basic usage is limited to 10MB or 20 pages per document, with Markdown output only.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
