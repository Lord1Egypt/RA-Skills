## Description: <br>
Render PDF pages to images, extract embedded images, and inspect PDF page metadata using PyMuPDF. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Maverick-AI-Tech](https://clawhub.ai/user/Maverick-AI-Tech) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and document automation users use this skill to render local PDF pages as image files, extract embedded PDF images, and inspect page dimensions or document metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF rendering and image extraction read caller-selected local PDF files and write generated files to disk. <br>
Mitigation: Use a dedicated output folder and review the generated files before relying on them downstream. <br>
Risk: The artifact describes annotation and redaction capabilities, but the included CLI exposes only info, export-images, and extract-images commands. <br>
Mitigation: Do not rely on this skill for annotation or redaction unless those commands are added and reviewed. <br>
Risk: The skill depends on the external PyMuPDF package. <br>
Mitigation: Pin or verify the PyMuPDF package version where supply-chain control matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Maverick-AI-Tech/pymupdf) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Files, Text] <br>
**Output Format:** [Markdown guidance with inline shell commands; generated operations write image files or print text summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local PDF paths and caller-selected output directories; page numbers are 0-indexed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
