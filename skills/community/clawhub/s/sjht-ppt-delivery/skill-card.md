## Description:

Convert an HTML slide deck to PDF and send it to a Feishu user as a file message.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aowind](https://clawhub.ai/user/aowind)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to turn generated HTML presentations into PDF files and deliver those files to a Feishu recipient through a bot account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send local files using stored Feishu bot credentials.

Mitigation: Use a tightly scoped Feishu bot account, confirm the destination user and exact filename before sending, and restrict uploads to generated workspace outputs.

Risk: The skill renders HTML with Chromium sandboxing disabled.

Mitigation: Avoid rendering untrusted HTML unless Chromium sandboxing or container isolation is added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aowind/skills/sjht-ppt-delivery)
- [Feishu tenant access token API endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal)
- [Feishu file upload API endpoint](https://open.feishu.cn/open-apis/im/v1/files)
- [Feishu message send API endpoint](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, files]

**Output Format:** [Markdown guidance with inline shell commands and generated PDF file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Chromium, puppeteer-core, pdf-lib, Python requests, Feishu bot credentials, and a Feishu recipient open_id.]

## Skill Version(s):

1.0.0 (source: release metadata and changelog, released 2026-03-20)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
