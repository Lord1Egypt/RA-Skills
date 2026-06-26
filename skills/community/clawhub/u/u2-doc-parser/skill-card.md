## Description: <br>
Parse documents using the UniDoc API for conversion to Markdown or JSON format, with synchronous and asynchronous modes and automatic status polling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaiccee](https://clawhub.ai/user/aaiccee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document-processing users use this skill to convert PDFs, Office documents, images, and text files into Markdown or JSON through the UniDoc API. It is intended for non-sensitive documents where cloud-based parsing is acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected documents are uploaded to UniDoc's UAT external service and processed on third-party servers. <br>
Mitigation: Use only non-sensitive test documents; do not submit private, regulated, confidential, or business-sensitive files. <br>
Risk: A changed UNIDOC_BASE_URL or UNIDOC_API_KEY value could route documents or credentials somewhere unintended. <br>
Mitigation: Check UNIDOC_BASE_URL and UNIDOC_API_KEY before running the skill. <br>
Risk: Using --force can overwrite or remove an existing output path. <br>
Mitigation: Use --force only when the selected output path is disposable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aaiccee/u2-doc-parser) <br>
- [Publisher profile](https://clawhub.ai/user/aaiccee) <br>
- [UniDoc API documentation](http://unidoc.uat.hivoice.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown or JSON content printed to stdout or saved to a user-selected output file, with progress and errors on stderr.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports synchronous conversion and asynchronous polling; uploads selected input files to the configured UniDoc service.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
