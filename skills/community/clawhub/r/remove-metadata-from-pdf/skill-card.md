## Description: <br>
Remove metadata from one or multiple PDFs by uploading them to the Solutions API, polling until completion, then returning download URLs for cleaned PDFs or a ZIP archive. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CrossServiceSolutions](https://clawhub.ai/user/CrossServiceSolutions) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and document workflows can use this skill to remove metadata from PDFs through Cross-Service-Solutions and retrieve cleaned PDF or ZIP download links. It is suited for documents the user is allowed to upload to that provider. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF contents are uploaded to an external service for processing. <br>
Mitigation: Use only documents that may be shared with Cross-Service-Solutions, and confirm the provider's privacy, retention, and access controls before uploading confidential or regulated files. <br>
Risk: The skill requires a bearer API key. <br>
Mitigation: Keep the API key private, avoid echoing or logging it, and verify the upload URL before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/CrossServiceSolutions/remove-metadata-from-pdf) <br>
- [Publisher profile](https://clawhub.ai/user/CrossServiceSolutions) <br>
- [Solutions API registration](https://login.cross-service-solutions.com/register) <br>
- [Solutions API endpoint](https://api.xss-cross-service-solutions.com/solutions/solutions) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [JSON result with job status, output file metadata, and download URLs; Markdown guidance may include shell commands for CLI use.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires one or more PDF files and a Solutions API key; multiple inputs may return multiple PDFs or a ZIP archive.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
