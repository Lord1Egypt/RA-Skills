## Description:

Work with S3-compatible object storage with proper security, lifecycle policies, and access patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill for concise operational guidance when configuring S3-compatible object storage access, lifecycle behavior, versioning, CORS, multipart uploads, replication, and provider-specific differences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Presigned URLs and S3 credentials can grant object access if exposed.

Mitigation: Treat presigned URLs and credentials as sensitive secrets, use the shortest practical URL expiration, and generate signed URLs server-side.

Risk: Incorrect public access settings can expose bucket contents.

Mitigation: Default to private access, review both account-level and bucket-level block settings, and prefer a CDN in front of public web assets.

Risk: Versioning, lifecycle, and multipart upload settings can create unexpected retention or cost.

Mitigation: Configure lifecycle rules for temporary objects, old versions, and incomplete multipart uploads, and check storage-tier minimum duration and transition costs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/s3)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands]

**Output Format:** [Markdown guidance with inline command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No code execution; the skill provides reference guidance for S3-compatible storage operations.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
