## Description: <br>
Uploads files such as images, PDFs, and documents to tmpfiles.org and returns temporary download links for sharing through messaging platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TurboS7](https://clawhub.ai/user/TurboS7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agents use this skill to create temporary public file links for screenshots, PDFs, or documents, especially when direct upload to a messaging platform fails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Accidental sharing of sensitive files through temporary public tmpfiles.org links. <br>
Mitigation: Confirm the exact file path and recipient before upload, and do not use the skill for sensitive, confidential, or permanent storage. <br>


## Reference(s): <br>
- [tmpfiles.org upload API endpoint](https://tmpfiles.org/api/v1/upload) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, API Calls] <br>
**Output Format:** [Markdown with Python, bash, and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces temporary public tmpfiles.org links that expire after about one hour; artifact notes a maximum file size of about 100MB.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
