## Description:

将本地 Markdown 文章转换为微信公众号 HTML，上传封面素材，并通过微信公众平台 API 创建草稿。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cnspica](https://clawhub.ai/user/cnspica)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to prepare local Markdown articles for WeChat Official Account draft review. It helps collect WeChat app credentials and article paths, run the upload workflow, and troubleshoot common WeChat API errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports exposed WeChat credentials in source and command-line usage.

Mitigation: Remove the hardcoded credential wrapper, rotate any exposed AppSecret, and avoid passing secrets on the command line before use.

Risk: The security scan reports under-disclosed draft-reading and export scripts.

Mitigation: Remove the draft export scripts unless they are explicitly required, and only run them where local plaintext draft exports are acceptable.

Risk: The skill can create or read WeChat Official Account drafts through authenticated API calls.

Mitigation: Review the scripts before installation and run them only with a WeChat account and workspace approved for that content.

## Reference(s):

- [微信公众号草稿 API 参考](references/wechat_api.md)
- [微信公众平台](https://mp.weixin.qq.com/)
- [Skill page](https://clawhub.ai/cnspica/skills/wechat-mp-draft-cnspica)
- [Publisher profile](https://clawhub.ai/user/cnspica)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline shell commands and parameter guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or update WeChat draft content through API calls when its scripts are run with user credentials.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
