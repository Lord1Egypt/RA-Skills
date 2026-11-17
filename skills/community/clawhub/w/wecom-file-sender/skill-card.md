## Description:

通过企业微信将本地目录中的文件（文档、图片、视频、语音）发送给指定用户，支持文件大小限制管理。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chongjie-ran](https://clawhub.ai/user/chongjie-ran)

### License/Terms of Use:

MIT-0

## Use Case:

Employees or agents operating in a WeCom-enabled workspace use this skill to locate local files and send documents, images, videos, or voice files to a specified user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can cause an agent to share local workspace or company-memory files through WeCom without clear authorization or confirmation safeguards.

Mitigation: Require an exact recipient and file path, confirm before every send, and apply the organization's data-sharing policy before emitting a MEDIA directive.

Risk: Sensitive company records, customer data, credentials, or regulated content may be exposed if files from memory or companywork paths are sent without review.

Mitigation: Treat memory and companywork paths as sensitive and avoid sending protected content unless policy explicitly permits sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chongjie-ran/skills/wecom-file-sender)
- [Publisher profile](https://clawhub.ai/user/chongjie-ran)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with MEDIA directives and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [MEDIA directives are emitted one file per line with a local file path; documented size limits cover images, videos, AMR voice files, and generic files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
