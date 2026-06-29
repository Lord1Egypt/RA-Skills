## Description: <br>
A WeChat Official Account operations skill for collecting topic data, planning article ideas, drafting and formatting posts, preparing account publishing details, and structuring post-publication review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luemery](https://clawhub.ai/user/luemery) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, operators, and developers use this skill to produce WeChat Official Account content workflows: research topics, choose titles, draft articles, generate Markdown or HTML previews, prepare publishing checklists, and review performance after posting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Drafts, publishing settings, or post-publication analysis may be inaccurate or unsuitable for public release. <br>
Mitigation: Review article drafts, cited sources, account settings, publish timing, and tracking metrics before posting or relying on results. <br>
Risk: Research and image-selection workflows may surface unauthorized copied content or media with unclear rights. <br>
Mitigation: Use public or authorized sources, verify data citations, and confirm image licensing before publication. <br>
Risk: Local configuration and generated workspace files may expose sensitive account or user information if secrets are stored there. <br>
Mitigation: Do not store passwords, API tokens, cookies, or private user data in local config files or generated workspaces. <br>
Risk: Generated public-facing content may include unsupported claims, especially in regulated topics such as health, finance, or legal advice. <br>
Mitigation: Fact-check names, dates, links, numerical claims, and regulated-topic statements before publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luemery/wechat-mp-publisher-pro) <br>
- [Content style reference](artifact/references/content-style.md) <br>
- [Design guide reference](artifact/references/design-guide.md) <br>
- [Article template](artifact/assets/article_template.md) <br>
- [Publishing checklist](artifact/assets/publish_checklist.md) <br>
- [Sogou WeChat search](https://weixin.sogou.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown articles and checklists, JSON/CSV research outputs, HTML previews, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local workspace outputs for collected data, article previews, article statistics, and account configuration templates; users should review all draft and publishing details before posting.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
