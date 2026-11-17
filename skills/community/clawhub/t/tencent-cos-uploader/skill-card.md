## Description:

Upload local files to Tencent COS and generate presigned links for browser preview and download.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hoyt-tian](https://clawhub.ai/user/hoyt-tian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to upload a chosen local file to a Tencent COS bucket and return signed view and download URLs for temporary sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Files are uploaded to a Tencent COS bucket and shared through signed URLs.

Mitigation: Confirm the selected local file, destination bucket, and object key before running the upload.

Risk: Long-lived signed URLs can be forwarded or exposed after generation.

Mitigation: Keep link expirations short and share generated URLs only with intended recipients.

Risk: Tencent COS credentials provide access to cloud storage resources.

Mitigation: Use least-privilege or temporary COS credentials and prefer environment variables over command-line secrets.

Risk: Using HTTP can expose request details for real data.

Mitigation: Use the default HTTPS scheme for real uploads and sharing links.

## Reference(s):

- [Tencent COS Uploader on ClawHub](https://clawhub.ai/hoyt-tian/skills/tencent-cos-uploader)
- [Publisher profile: hoyt-tian](https://clawhub.ai/user/hoyt-tian)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper script emits JSON containing bucket, region, object key, local file path, file size, expiration, generation timestamp, presigned view URL, presigned download URL, and Tencent COS upload response.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
