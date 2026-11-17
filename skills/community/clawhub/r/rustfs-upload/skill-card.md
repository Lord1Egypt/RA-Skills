## Description:

Uploads selected images or files to RustFS-compatible object storage and returns a public access URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wzwei1990](https://clawhub.ai/user/wzwei1990)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to upload a selected local file to RustFS or compatible S3-style object storage and receive a shareable URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish selected local files to object storage and return public links.

Mitigation: Confirm each file is intended for upload and verify the public domain, bucket, and object path before sharing the returned URL.

Risk: The skill may change persistent RustFS CLI configuration by setting the rustfs-temp alias.

Mitigation: Use narrowly scoped credentials and review the local rc alias configuration before and after use.

Risk: The skill can create a storage bucket automatically when the target bucket is missing.

Mitigation: Pre-create and authorize the intended bucket, or confirm automatic bucket creation is acceptable for the environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wzwei1990/skills/rustfs-upload)
- [ClawHub publisher profile](https://clawhub.ai/user/wzwei1990)

## Skill Output:

**Output Type(s):** [shell commands, configuration, text]

**Output Format:** [JSON result with upload status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires rc, jq, RustFS endpoint credentials, bucket, and public domain configuration.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
