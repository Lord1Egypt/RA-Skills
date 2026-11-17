## Description:

Sends generated documents, local files, or screenshots to messaging platforms, with Feishu supported through file upload and message send steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlong800](https://clawhub.ai/user/wlong800)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent choose a generated file, specified local file, or screenshot and send it to a messaging recipient, primarily through Feishu file upload.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload arbitrary local files or screenshots to Feishu without a clear confirmation gate.

Mitigation: Require confirmation of the exact file path, recipient, and platform before every send, and avoid sending screenshots or generated reports until the user has reviewed them for sensitive data.

Risk: The skill documentation recommends plaintext persistence of FEISHU_APP_SECRET in shell startup files.

Mitigation: Use a credential manager or temporary per-command environment injection, and avoid storing FEISHU_APP_SECRET in ~/.zshrc or ~/.bashrc.

## Reference(s):

- [Feishu Open Platform](https://open.feishu.cn/app)
- [Feishu Tenant Access Token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu File Upload API](https://open.feishu.cn/open-apis/im/v1/files)
- [Feishu Message Send API](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown instructions with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger Feishu API calls that upload a selected local file before sending a message.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
