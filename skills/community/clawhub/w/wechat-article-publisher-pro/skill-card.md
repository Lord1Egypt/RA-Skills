## Description: <br>
Helps agents prepare, format, publish, and manage WeChat Official Account articles, materials, statistics, and comments through a Python command-line tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobewin](https://clawhub.ai/user/tobewin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and content teams use this skill to automate WeChat Official Account article workflows, including HTML rendering, draft creation, media upload, publishing, statistics retrieval, and comment management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Delete and publish actions can remove or expose WeChat Official Account content. <br>
Mitigation: Require the agent to show exact target IDs, titles, and intended action before draft, published article, material, or comment deletion and before publishing. <br>
Risk: Drafts, media, article content, and credentials may be sensitive account data. <br>
Mitigation: Use the skill only with content intended for WeChat, keep credentials in environment variables, and avoid sending sensitive drafts or media unless publication or upload is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tobewin/skills/wechat-article-publisher-pro) <br>
- [WeChat Official Account API documentation](https://developers.weixin.qq.com/doc/subscription/api/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON payload examples, and Python CLI usage.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WECHAT_APP_ID and WECHAT_APP_SECRET. Commands can call WeChat APIs and return JSON responses, media IDs, publish IDs, URLs, status text, or rendered HTML.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release metadata; artifact frontmatter reports 1.0.7) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
