## Description: <br>
Upload a local file to tmpfiles.org using Python standard library only, then return a direct download link in strict JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[donigwapo](https://clawhub.ai/user/donigwapo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workflow operators use this skill to upload an explicitly selected local workspace file to tmpfiles.org and receive a temporary public download URL as strict JSON for automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated tmpfiles.org link is public and temporary, so uploading sensitive files can expose private information. <br>
Mitigation: Confirm the exact file path before upload and avoid secrets, credentials, IDs, financial records, contracts, or private documents unless public sharing is intentional. <br>
Risk: The skill publishes a user-selected local file to an external hosting service. <br>
Mitigation: Use it only when public temporary file hosting is acceptable; choose private storage for secure or long-term sharing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/donigwapo/tmpfiles-upload-stdlib) <br>
- [tmpfiles.org](https://tmpfiles.org) <br>
- [tmpfiles.org upload API](https://tmpfiles.org/api/v1/upload) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [Strict JSON object with success or failure fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a temporary public download URL on success; returns an error object when the file is missing or upload fails.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
