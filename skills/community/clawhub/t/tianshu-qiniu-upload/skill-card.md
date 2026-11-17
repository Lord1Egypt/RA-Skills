## Description:

Uploads local files such as images, HTML pages, and documents to Qiniu Cloud storage and returns a publicly accessible CDN URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangshengli0421](https://clawhub.ai/user/wangshengli0421)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill when they need an agent to upload a reviewed local file to a configured Qiniu Cloud bucket and return a shareable public URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured Qiniu credentials allow uploads to the target bucket, and uploaded files become publicly accessible through the configured domain.

Mitigation: Confirm the exact local path and intended destination before upload; do not upload secrets, private documents, tokens, internal reports, or unreviewed files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangshengli0421/skills/tianshu-qiniu-upload)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text URL with optional Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires QINIU_ACCESS_KEY, QINIU_SECRET_KEY, QINIU_BUCKET, and QINIU_DOMAIN; QINIU_PREFIX is optional and defaults to uploads.]

## Skill Version(s):

1.0.2 (source: server release evidence and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
