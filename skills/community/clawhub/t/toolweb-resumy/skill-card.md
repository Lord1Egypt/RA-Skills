## Description: <br>
Generate professional resumes and cover letters from structured data with optional resume parsing capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Recruiters, HR teams, career platforms, and agent developers use this skill to generate resumes and tailored cover letters from structured candidate data, parse unstructured resume content, and retrieve generated document files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The service handles sensitive resume contents and contact details without enough evidence about privacy, consent, retention, or access controls. <br>
Mitigation: Use only when appropriate for the data involved and confirm the provider's privacy policy, retention and deletion behavior, consent handling, and access controls before sending real applicant data. <br>
Risk: Generated document download URLs may expose resumes or cover letters if download scope and authorization are not limited to the requesting user. <br>
Mitigation: Confirm downloads are access-controlled and limited to the user's own generated files before using the skill with confidential applicant information. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/toolweb-resumy) <br>
- [Resumy API Documentation](https://api.toolweb.in:8166/docs) <br>
- [Resumy API Route](https://api.toolweb.in/tools/resumy) <br>
- [ToolWeb](https://toolweb.in) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Files, Markdown] <br>
**Output Format:** [JSON responses with generated document filenames, download URLs, and structured resume data; downloaded outputs are resume or cover letter files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires candidate contact and resume content; generated files are retrieved by filename through a download endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
