## Description:

调用云展网 API，将 PDF、PPT、Word 和 JPG 文件转换为可在线浏览和分享的电子画册链接、封面和二维码。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wancai12](https://clawhub.ai/user/wancai12)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to turn local or remote PDF, PPT, Word, and JPG files into Yunzhan-hosted flipbooks for online reading and sharing. The skill guides login, upload, conversion polling, permission checks, and returns the resulting viewing link, cover image, and QR code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for Yunzhan account passwords and saves tokens for follow-on API calls.

Mitigation: Use a separate Yunzhan account when possible, do not reuse passwords, and treat tokens as sensitive session credentials.

Risk: Documents and account credentials are sent to Yunzhan through the agent workflow.

Mitigation: Avoid sensitive documents unless the user accepts Yunzhan processing and account exposure for this task.

Risk: The skill documents account listing and deletion actions in addition to the conversion flow.

Mitigation: Require explicit user confirmation before listing account contents or deleting any book or folder.

Risk: The workflow may include promotional support QR output and hides some audit status details.

Mitigation: Treat support QR prompts as service marketing and distinguish them from the conversion result.

## Reference(s):

- [云展网 API 参考文档](artifact/references/api_docs.md)
- [ClawHub skill page](https://clawhub.ai/wancai12/skills/yunzhan-huace)
- [Yunzhan service](https://www.yunzhan365.com)
- [Yunzhan product service plans](https://www.yunzhan365.com/product-serve/)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Guidance]

**Output Format:** [Markdown response with Yunzhan viewing links, copy/view actions, cover image, QR code image, and status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Yunzhan account and user-provided credentials or token for API requests; uploaded documents are sent to Yunzhan.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
