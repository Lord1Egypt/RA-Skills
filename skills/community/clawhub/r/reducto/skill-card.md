## Description: <br>
Reducto provides a document processing API integration through Maton-managed authentication for parsing, extraction, splitting, uploads, jobs, pipelines, and PDF or DOCX edits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call Reducto document workflows from ClawHub, including parsing documents, extracting structured fields, splitting content into sections, editing PDFs or DOCX files, uploading files, and polling asynchronous jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Document data is sent to Maton and Reducto for processing. <br>
Mitigation: Use the skill only when that transfer is acceptable, and avoid sensitive or regulated documents unless the user has approved the transfer and compliance requirements are satisfied. <br>
Risk: MATON_API_KEY is a sensitive credential required for all requests. <br>
Mitigation: Use a dedicated API key where possible, keep the key out of logs and chat transcripts, and rotate it if exposure is suspected. <br>
Risk: Uploads, document edits, connection changes, and delete operations can change documents or account state. <br>
Mitigation: Require clear user confirmation before any upload, create, update, edit, connection-management, or delete operation, including the target resource and intended effect. <br>


## Reference(s): <br>
- [ClawHub Reducto Skill](https://clawhub.ai/byungkyu/reducto) <br>
- [Maton](https://maton.ai) <br>
- [Reducto Documentation](https://docs.reducto.ai) <br>
- [Reducto API Reference](https://docs.reducto.ai/api-reference) <br>
- [Reducto Studio](https://studio.reducto.ai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration, API requests] <br>
**Output Format:** [Markdown with inline Bash, Python, JavaScript, JSON, and HTTP examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access and MATON_API_KEY; API responses may include processed document content, job status, usage data, and presigned upload URLs.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence; artifact frontmatter says 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
