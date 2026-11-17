## Description:

Uploads local files to Qiniu Object Storage and returns either a public delivery URL or a time-limited signed private URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[showtimewalker](https://clawhub.ai/user/showtimewalker)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workflow agents use this skill as a delivery step when an existing or generated local file needs to be uploaded to Qiniu Object Storage and returned as a shareable link. It is especially useful for workflows that must respect bucket privacy by returning signed URLs for private buckets and public URLs for public buckets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected local files may be uploaded to Qiniu and become accessible through the configured delivery URL.

Mitigation: Use the skill only for files intended for object-storage delivery, and verify the bucket, domain, and public/private setting before sharing links.

Risk: Signed private URLs are shareable access tokens until they expire.

Mitigation: Use short expirations for private links and share generated URLs only with intended recipients.

Risk: Large uploads may consume significant memory or hang because the security evidence notes no streaming and no network timeouts.

Mitigation: Avoid very large files unless the runtime can tolerate the memory and network behavior, or add streaming and timeout controls before deployment.

## Reference(s):

- [Usage Guide](artifact/references/usage.md)
- [ClawHub Skill Page](https://clawhub.ai/showtimewalker/skills/qiniu-object-storage)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The upload scripts return JSON fields such as storage_provider, bucket, object_key, access_mode, delivery_url, and optional public_url, private_url, base_url, and expires_in.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
