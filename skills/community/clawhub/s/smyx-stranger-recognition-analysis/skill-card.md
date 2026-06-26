## Description: <br>
Identifies strangers in surveillance video or images through facial comparison and returns structured recognition reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security operators, property managers, and access-control teams use this skill to analyze authorized surveillance media, identify known or unfamiliar faces, enroll approved people into a face database, and review cloud-hosted recognition report history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud facial-recognition analysis may upload surveillance media and biometric face data to a provider-controlled service. <br>
Mitigation: Use only with authorization for the people, locations, and media involved; confirm consent, retention, and provider data-handling requirements before installation. <br>
Risk: Enrollment can persist face records in a cloud database under the supplied open-id. <br>
Mitigation: Enroll people only when there is a clear operational need, use a controlled open-id, and review how enrolled records can be accessed, retained, or removed. <br>
Risk: The security evidence flags under-disclosed account, token, local persistence, enrollment, and API-documentation risks. <br>
Mitigation: Review configuration files and credentials before use, avoid storing sensitive tokens in shared workspaces, and verify API behavior against the provider before relying on reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/smyx-stranger-recognition-analysis) <br>
- [Skill API reference](references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON report text, with Python command examples and configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an open-id plus an authorized video, image, or media URL; can optionally enroll a named person into the face database.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
