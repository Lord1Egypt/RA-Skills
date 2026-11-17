## Description:

Upload files to UCloud US3 (UFile) object storage and generate signed download URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qianjunye](https://clawhub.ai/user/qianjunye)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to upload generated files from a sandbox to a configured UCloud US3 bucket and return time-limited signed download links to users.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads generated files to an external UCloud US3 bucket and treats upload as the default way to share files.

Mitigation: Install only when external uploads are intended, avoid secrets or private documents, and require explicit approval before each upload.

Risk: Signed URLs are shareable external links.

Mitigation: Treat generated URLs as sensitive for their validity period and share them only with intended recipients.

Risk: The upload helper installs the unpinned ufile SDK at runtime if it is missing.

Mitigation: Pin and provision the ufile SDK before runtime instead of relying on automatic installation.

Risk: Incorrect bucket or endpoint configuration can send files to an unintended storage location.

Mitigation: Validate the configured bucket endpoint before enabling uploads.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qianjunye/skills/us3-uploader-encrypted)
- [US3 CLI Configuration Guide](references/us3_config.md)
- [UCloud US3 CLI documentation](https://docs.ucloud.cn/ufile/tools/us3cli/prepare)
- [UCloud us3cli releases](https://github.com/ucloud/us3cli/releases)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and signed URL text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces signed download URLs valid for 7 days after upload.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
