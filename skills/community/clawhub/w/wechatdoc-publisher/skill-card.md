## Description:

Helps an agent turn Markdown articles and cover images into WeChat Official Account draft submissions, including credential setup guidance, access token retrieval, image upload, Markdown-to-HTML conversion, and draft creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liboss504](https://clawhub.ai/user/liboss504)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, operators, and developers use this skill to prepare and submit Markdown-based articles as WeChat Official Account drafts. It is suited for workflows that need cover-image handling, WeChat API calls, draft JSON construction, and publication checks before final review in the WeChat backend.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs users to add a fixed IP address, 112.8.202.216, to the WeChat API allowlist without server-resolved evidence explaining why that address is required.

Mitigation: Only allowlist the actual egress IP of the environment running the scripts unless the publisher provides a verifiable reason to use the fixed address.

Risk: The scripts read AppID and AppSecret from a local wechat_credentials.json file, which can expose account credentials if stored in repositories or shared workspaces.

Mitigation: Keep the credential file out of version control and shared directories, restrict file permissions, rotate exposed secrets, and use dedicated low-privilege operating credentials where possible.

Risk: Running publish.py can upload cover media and submit a draft to the configured WeChat Official Account.

Mitigation: Review the Markdown content, cover image, account credentials, and generated draft details before executing the publish script.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liboss504/skills/wechatdoc-publisher)
- [WeChat Official Accounts Platform](https://mp.weixin.qq.com)
- [WeChat API base](https://api.weixin.qq.com)
- [WeChat API reference](artifact/references/api_ref.md)
- [Credential configuration guide](artifact/references/credentials_guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and generated WeChat draft/API outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local draft JSON, compressed image files, uploaded media identifiers, and WeChat draft submissions when the scripts are run with valid credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact version record)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
