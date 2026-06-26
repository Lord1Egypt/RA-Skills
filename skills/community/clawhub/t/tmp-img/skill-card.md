## Description: <br>
Uploads a selected image to the temporary third-party image host imgland.net, returning a public image URL and expiration details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maoruibin](https://clawhub.ai/user/maoruibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to upload a local image for temporary public sharing and receive a machine-readable response with the image URL, file metadata, expiration timestamp, and delete URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/maoruibin/tmp-img) <br>
- [imgland image upload API endpoint](https://api.imgland.net/v1/images) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON response with public URL, image identifier, filename, file size, expiration timestamp, and delete URL, plus concise user-facing guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should treat the public image URL and delete URL as sensitive links; users should avoid uploading secrets, credentials, private screenshots, documents, or sensitive personal data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
