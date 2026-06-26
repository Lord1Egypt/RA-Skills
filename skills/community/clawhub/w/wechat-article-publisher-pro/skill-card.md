## Description: <br>
Wechat Publisher helps agents turn user-provided URLs, Markdown, Word/PDF files, or topic prompts into formatted WeChat Official Account articles and create, publish, manage, or inspect live-account content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobewin](https://clawhub.ai/user/tobewin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, marketing operators, and developers use this skill to prepare WeChat Official Account drafts or articles from web, file, or prompt input and manage publication workflows with their own account credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish or delete WeChat public-account content using live account credentials. <br>
Mitigation: Require explicit user confirmation for publish and delete actions, test with drafts first, and use the least-privileged account credentials available. <br>
Risk: WeChat AppID, AppSecret, access tokens, and logs are sensitive. <br>
Mitigation: Store credentials only in trusted environment variables or local config, avoid sharing logs that may contain account identifiers or API responses, and rotate credentials after exposure. <br>
Risk: URL ingestion can pull content from internal, private, or untrusted pages. <br>
Mitigation: Use only public or authorized URLs and review extracted content before it is rendered, drafted, or published. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tobewin/wechat-article-publisher-pro) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/tobewin) <br>
- [WeChat Official Accounts platform](https://mp.weixin.qq.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration examples, HTML article content, Python code, and JSON-like API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create drafts, publish content, delete drafts or published articles, and retrieve article/account data when valid WeChat credentials are configured.] <br>

## Skill Version(s): <br>
1.0.4 (source: frontmatter, ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
