## Description: <br>
Upload files to Cloudflare R2, AWS S3, or any S3-compatible storage and generate secure presigned download links with configurable expiration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[julianengel](https://clawhub.ai/user/julianengel) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to upload local files to Cloudflare R2, AWS S3, or compatible storage and return short-lived download links. It also supports listing bucket contents, generating new links for existing objects, and deleting uploaded objects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload user-specified local files to a cloud bucket, which may expose sensitive data if used on the wrong file. <br>
Mitigation: Review the file path and bucket before upload, avoid uploading sensitive files unless intended, and use short presigned URL expirations. <br>
Risk: Cloud storage credentials in the local configuration can grant access to bucket contents if they are over-scoped or exposed. <br>
Mitigation: Use bucket-scoped, least-privilege credentials and keep the local configuration file private. <br>
Risk: Delete requests remove the specified remote object immediately. <br>
Mitigation: Double-check the bucket and object key before approving delete operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/julianengel/r2-upload) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [Plain text responses with generated URLs, object listings, status messages, and setup guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include short-lived presigned URLs, public URLs when requested, bucket object metadata, and delete confirmations.] <br>

## Skill Version(s): <br>
1.0.4 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
