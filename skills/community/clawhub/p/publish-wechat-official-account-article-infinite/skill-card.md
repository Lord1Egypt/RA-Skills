## Description: <br>
Guides an agent through publishing articles for the "无限" author in WeChat Official Accounts, including article formatting, cover image generation, originality and reward settings, draft saving, preview, and publication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[infiniteask](https://clawhub.ai/user/infiniteask) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators or delegated operators use this skill to help an agent prepare and publish an article in a logged-in WeChat Official Account session for the "无限" author. It is intended for guided browser operation covering title, author, body formatting, cover image, summary, originality declaration, reward settings, collection selection, draft saving, preview, and final publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to publish publicly from a logged-in WeChat Official Account without a clear final approval checkpoint. <br>
Mitigation: Require the agent to stop before final publication, display the active account, title, author, collection, originality setting, reward setting, and planned publish action, then wait for explicit user approval. <br>
Risk: The workflow may encounter login, password, MFA, scan, or phone verification steps during preview or publishing. <br>
Mitigation: Do not enter passwords, MFA codes, or scan confirmations into chat; the account owner should complete authentication directly in the browser. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/infiniteask/publish-wechat-official-account-article-infinite) <br>
- [WeChat Official Account platform](https://mp.weixin.qq.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, Markdown] <br>
**Output Format:** [Markdown procedural guidance for browser-based publishing workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide actions that save drafts, preview content, and publish publicly from an authenticated WeChat Official Account session.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.8.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
