## Description: <br>
Uploads selected image attachments to stardots.io cloud storage using configured Stardots credentials and MD5 request signing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keepchen](https://clawhub.ai/user/keepchen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill to back up image attachments from an agent session to a Stardots storage space. It is intended for workflows where uploaded image URLs or upload status messages are useful after the transfer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected image attachments and their contents are sent to Stardots. <br>
Mitigation: Install only for workflows where sending those images to Stardots is intended, and avoid confidential or regulated images unless appropriate controls are in place. <br>
Risk: The security review reports an unsafe shell-command upload path that deserves review before installation. <br>
Mitigation: Use a dedicated, least-privilege Stardots API key and prefer a patched version that uploads through a structured HTTP client rather than interpolating paths and secrets into a shell command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/keepchen/stardots-backup) <br>
- [Stardots](https://stardots.io) <br>
- [Stardots OpenAPI documentation](https://stardots.io/en/documentation/openapi) <br>


## Skill Output: <br>
**Output Type(s):** [text] <br>
**Output Format:** [Plain text status messages with uploaded image URLs when uploads succeed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include per-image success, failure, or missing-configuration messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, skill.yaml, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
