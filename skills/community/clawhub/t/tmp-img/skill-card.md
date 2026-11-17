## Description:

Uploads a selected local image file to the imgland.net temporary image host, defaulting to a 30-day expiration and returning a public link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maoruibin](https://clawhub.ai/user/maoruibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to temporarily upload a single image and return a public URL, expiration timestamp, file metadata, and delete URL for sharing or short-lived inspection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload any readable local file to a public third-party host without validating that the file is an image or requiring a clear confirmation.

Mitigation: Verify the exact file path before execution and do not upload screenshots or files containing secrets, credentials, personal data, or internal documents.

Risk: The returned delete_url may allow anyone who has it to delete the hosted image.

Mitigation: Treat delete_url as sensitive and share only the public image URL unless deletion access is intentionally needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maoruibin/skills/tmp-img)
- [imgland.net image upload API endpoint](https://api.imgland.net/v1/images)

## Skill Output:

**Output Type(s):** [shell commands, JSON, guidance]

**Output Format:** [JSON object with public image URL, image ID, filename, file size, expiration timestamp, and delete URL; agents may summarize the URL and expiry in text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uploads one readable local file per invocation; default expiration is 30 days and may be configured with values such as 1d, 7d, or 30d.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
