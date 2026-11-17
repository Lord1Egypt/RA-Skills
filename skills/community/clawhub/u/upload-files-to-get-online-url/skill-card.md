## Description:

Uploads local files to Tencent Cloud COS and returns a direct object URL, a 24-hour signed URL, and the COS object key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parsonssss](https://clawhub.ai/user/parsonssss)

### License/Terms of Use:


## Use Case:

Developers and automation agents use this skill to upload images, documents, videos, or other local files to Tencent Cloud COS and capture shareable object URLs for hosting or file-sharing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Tencent Cloud credentials for COS uploads.

Mitigation: Use least-privilege, preferably short-lived credentials limited to the intended bucket and path prefix, and prefer environment variables or a protected credential provider over command-line secret flags.

Risk: Printed signed URLs can grant temporary access to private bucket objects.

Mitigation: Treat signed URLs as temporary credentials and avoid exposing them in logs, chats, tickets, or other shared output.

Risk: Uploaded files may become accessible depending on bucket permissions and sharing rules.

Mitigation: Do not upload sensitive files unless bucket access, retention, and sharing rules are understood and approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/parsonssss/skills/upload-files-to-get-online-url)
- [Publisher profile](https://clawhub.ai/user/parsonssss)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text status output with URLs, a COS object key, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May print direct and signed URLs; signed URLs are temporary credentials with a 24-hour expiration.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
