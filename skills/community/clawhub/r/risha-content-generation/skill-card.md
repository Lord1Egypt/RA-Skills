## Description: <br>
Risha.ai Content Generation helps agents discover available Risha.ai capabilities, prepare valid requests, estimate credits, run generation jobs, and retrieve text or media outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aimedialab](https://clawhub.ai/user/aimedialab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to automate authenticated Risha.ai content-generation workflows, including capability discovery, request preparation, credit estimation, job polling, and retrieval of generated text, audio, image, video, or multimodal outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive Risha.ai account credentials or an authorization header, and the security summary notes that a helper command may expose session credentials. <br>
Mitigation: Use a prebuilt authorization header where possible, protect environment variables, avoid the login subcommand unless the exposure is fixed or logs are redacted, and remove credentials from shared output. <br>
Risk: Generation requests can spend account credits. <br>
Mitigation: Review the credit preview or run an estimate before submitting generation requests, and confirm the projected cost before creating content. <br>
Risk: Refreshing the capability catalog can persist account-specific capability data. <br>
Mitigation: Do not refresh catalogs into shared or committed directories when they reveal private workspace capabilities; store refreshed snapshots only in an appropriate private workspace. <br>


## Reference(s): <br>
- [Risha API Reference](references/risha-api.md) <br>
- [Current Risha Capabilities](references/current-capabilities.md) <br>
- [Current Risha Capabilities JSON](references/current-capabilities.json) <br>
- [Risha OpenAPI Document](https://adminxcore-api.risha.ai/api/docs/?format=openapi) <br>
- [ClawHub Skill Page](https://clawhub.ai/aimedialab/risha-content-generation) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, API calls] <br>
**Output Format:** [Markdown guidance with JSON payloads, shell commands, API responses, generated text, and media asset URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return generated content, media metadata, thumbnails, credit previews, job statuses, and failure details from Risha.ai.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
