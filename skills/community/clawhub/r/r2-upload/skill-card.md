## Description:

Upload files to Cloudflare R2, AWS S3, or any S3-compatible storage and generate secure presigned download links with configurable expiration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[julianengel](https://clawhub.ai/user/julianengel)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to upload selected local files to Cloudflare R2, AWS S3, MinIO, or S3-compatible storage, then return temporary download links for sharing. It also supports listing bucket contents, deleting objects, and generating new presigned URLs for existing objects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use bucket-scoped R2/S3 credentials to upload selected local files, list objects, generate shareable links, and delete remote objects.

Mitigation: Use a dedicated bucket, least-privilege credentials, HTTPS endpoints, and review agent requests before upload or delete operations.

Risk: Generated links can expose uploaded files until expiration, and public URL mode can expose files without a signature.

Mitigation: Keep URL expirations short, avoid public links unless intended, and do not use the skill for sensitive files unless the storage destination and invoking workflow are trusted.

Risk: Cloud credentials are stored in a local configuration file.

Mitigation: Verify that the configuration file is owner-only readable, rotate credentials after suspected compromise, and avoid committing credential files to source control.

Risk: The artifact documents limited safeguards around large uploads, file type restrictions, rate limiting, content scanning, and custom object keys.

Mitigation: Apply external bucket policies, quotas, logging, and operational review for file paths, object keys, file types, and upload volume.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/julianengel/skills/r2-upload)
- [Cloudflare Dashboard](https://dash.cloudflare.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text tool responses with URLs and status messages; Markdown documentation with YAML and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated download URLs are short-lived by default unless public URL mode is explicitly used.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
