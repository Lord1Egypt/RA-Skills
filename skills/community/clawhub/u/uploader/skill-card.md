## Description: <br>
Upload a local file to Astron Claw Bridge and return a public download URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when a selected local file needs to be uploaded and represented as a shareable download URL for retrieval, embedding, or handoff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected local files are sent to a remote upload service and may be exposed through a public download link. <br>
Mitigation: Upload only files intended for sharing, avoid sensitive documents unless access controls are confirmed, and review the returned download URL before distribution. <br>
Risk: The upload destination and authorization token come from local OpenClaw bridge configuration. <br>
Mitigation: Verify the configured host and bearer token before use, and install the skill only when the upload service is trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/uploader) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text upload result containing file metadata and a download URL] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns the uploaded file name, MIME type, file size, session ID, and download URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
