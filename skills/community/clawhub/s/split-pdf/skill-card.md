## Description: <br>
Split a single PDF into multiple parts. Supports page ranges, per-page splitting, and fixed chunk splitting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rishabhdugar](https://clawhub.ai/user/rishabhdugar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document workflow agents use this skill to call PDF API Hub to split a PDF by page ranges, individual pages, or fixed chunks and receive the split PDFs as a zip output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF files or public PDF URLs provided to the skill are sent to pdfapihub.com, and outputs may be hosted there. <br>
Mitigation: Avoid confidential, regulated, or proprietary documents unless the provider's privacy, retention, deletion, and access-control practices have been reviewed and approved. <br>
Risk: The skill requires a PDF API Hub API key. <br>
Mitigation: Use a limited API key where possible, keep it out of shared prompts and files, and rotate it if exposure is suspected. <br>
Risk: Returned output links may be accessible outside the local agent environment until provider deletion. <br>
Mitigation: Limit sharing of returned file URLs and retrieve or remove generated outputs according to the provider's retention process. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rishabhdugar/split-pdf) <br>
- [PDF API Hub documentation](https://pdfapihub.com/docs) <br>
- [PDF API Hub](https://pdfapihub.com) <br>
- [Split PDF API endpoint](https://pdfapihub.com/api/v1/pdf/split) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with JSON request examples and bash commands; API responses can return zip file URLs, files, or base64 content.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a CLIENT-API-KEY header. Inputs may be a public PDF URL, a base64 PDF, or multipart file upload; limits are 200 pages per document and 100 output chunks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
