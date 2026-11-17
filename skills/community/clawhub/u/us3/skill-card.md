## Description:

Upload files to UCloud US3 object storage and generate public URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qianjunye](https://clawhub.ai/user/qianjunye)

### License/Terms of Use:

ISC

## Use Case:

Developers and agents use this skill to upload local files such as images, videos, documents, audio, and archives to UCloud US3 and return shareable public URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public file uploads can expose secrets, personal data, or confidential files.

Mitigation: Upload only files that are intended to be public, and review file contents before running the uploader.

Risk: Credential-bearing requests depend on the configured bucket host, which the security evidence says is not validated as UCloud.

Mitigation: Verify US3_BUCKET is exactly the expected UCloud US3 bucket domain before installation or execution.

Risk: UCloud credentials may grant broader access than the upload workflow requires.

Mitigation: Use a dedicated, least-privilege UCloud key restricted to the intended bucket.

Risk: The security guidance calls out an old dependency stack.

Mitigation: Prefer a revised release that updates dependencies before broad deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qianjunye/skills/us3)
- [UCloud UFile product page](https://www.ucloud.cn/site/product/ufile.html)
- [UCloud website](https://www.ucloud.cn/)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [JSON upload result or plain URL string]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The --url-only option emits only the public URL; default output includes success, url, key, bucket, size or status fields depending on upload path.]

## Skill Version(s):

1.0.0 (source: release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
