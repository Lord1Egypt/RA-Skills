## Description: <br>
Uploads images or files to RustFS or S3-compatible object storage and returns a public access URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wzwei1990](https://clawhub.ai/user/wzwei1990) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to upload a selected local file to RustFS or compatible object storage and return a JSON result containing the public URL, bucket, object key, file size, and endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected local files may be uploaded to RustFS or S3-compatible storage and exposed through a public URL. <br>
Mitigation: Run only with files intended for publication and verify the endpoint, bucket, and public domain before use. <br>
Risk: Storage credentials may be persisted through the rc alias used for uploads. <br>
Mitigation: Use least-privilege credentials and remove or rotate the rustfs-temp alias after use if credentials should not remain configured. <br>
Risk: The skill may create a storage bucket, and file expiration is not guaranteed by the upload script. <br>
Mitigation: Confirm bucket creation is acceptable and rely only on independently configured bucket lifecycle policies for expiration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wzwei1990/rustfs-upload) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Configuration] <br>
**Output Format:** [JSON result with command-line status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires rc, jq, RustFS endpoint and bucket settings, storage credentials, and a public domain.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
