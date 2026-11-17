## Description:

专门用于"无限"作者发表公众号文章的技能，包含完整的文章发布流程、格式要求和操作规范。

This skill is ready for commercial/non-commercial use.

## Publisher:

[infiniteask](https://clawhub.ai/user/infiniteask)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to guide an agent through publishing an "无限" article to a WeChat Official Account, including formatting, cover image selection, original-content declaration, reward settings, collection selection, draft saving, preview, and publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to publish publicly from an authenticated WeChat Official Account and enable rewards without a clear final approval step.

Mitigation: Require explicit user approval of the final article content, target collection, original declaration, reward setting, and publish action before enabling rewards or clicking publish.

Risk: The workflow depends on the agent interpreting WeChat page state correctly, including checkbox state, browser tabs, draft save status, and confirmation dialogs.

Mitigation: Verify visible page text and status messages before continuing, save a draft before preview or publication, and pause for user verification when the UI state is ambiguous.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/infiniteask/skills/publish-wechat-official-account-article-infinite)
- [ClawHub publisher profile](https://clawhub.ai/user/infiniteask)

## Skill Output:

**Output Type(s):** [guidance, text]

**Output Format:** [Markdown instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides browser-based WeChat Official Account publishing and asks the user to authenticate or verify when required.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
