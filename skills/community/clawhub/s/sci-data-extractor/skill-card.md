## Description: <br>
AI-powered tool for extracting structured data from scientific literature PDFs. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[JackKuo666](https://clawhub.ai/user/JackKuo666) <br>

### License/Terms of Use: <br>
CC BY 4.0 <br>


## Use Case: <br>
Researchers and developers use this skill to extract structured values, tables, and literature-review fields from scientific paper PDFs into Markdown or CSV for research workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF content may be sent to the configured LLM provider and to Mathpix when Mathpix OCR is enabled. <br>
Mitigation: Use the skill only with documents allowed by the relevant provider terms, and avoid confidential or unpublished papers unless those terms permit the upload. <br>
Risk: Installer commands that pipe remote scripts into a shell can reduce install hygiene. <br>
Mitigation: Use a virtual environment and prefer safer dependency installation methods where practical. <br>
Risk: AI-extracted scientific data may be incomplete or incorrect. <br>
Mitigation: Validate extracted results against the original literature before using them in downstream research or publications. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/JackKuo666/sci-data-extractor) <br>
- [CC BY 4.0 license](https://creativecommons.org/licenses/by/4.0/) <br>
- [Mathpix OCR API](https://api.mathpix.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; extraction outputs are Markdown tables or CSV files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses configured LLM providers and optional Mathpix OCR; users should validate extracted data.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
