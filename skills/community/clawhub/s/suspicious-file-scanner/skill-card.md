## Description: <br>
Analyzes uploaded files to detect suspicious characteristics and potential security threats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security teams and developers use this skill to upload files to a remote scanning API and receive threat indicators, confidence scores, and handling recommendations before accepting or quarantining files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Files are uploaded to api.mkkpro.com for analysis. <br>
Mitigation: Do not upload secrets, personal data, proprietary documents, or regulated material unless third-party handling has been approved. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/suspicious-file-scanner) <br>
- [API Docs](https://api.mkkpro.com:8013/docs) <br>
- [API Route](https://api.mkkpro.com/security/suspicious-file-scanner) <br>
- [ToolWeb](https://toolweb.in) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance for calling a multipart file scanning endpoint and interpreting JSON threat analysis results.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
