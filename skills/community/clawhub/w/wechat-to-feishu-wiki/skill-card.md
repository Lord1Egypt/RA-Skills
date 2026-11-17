## Description:

Fetch WeChat public-article content and save it into a user-provided Feishu Wiki location.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gift-is-coding](https://clawhub.ai/user/gift-is-coding)

### License/Terms of Use:

MIT-0

## Use Case:

External users and knowledge-base maintainers use this skill to archive one or more WeChat public-account articles into a user-selected Feishu Wiki node. It asks for the destination Wiki link, checks access, extracts visible article content, writes a child page, and reports created page links or failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes copied article text into the destination Feishu Wiki, so an incorrect or overly broad target Wiki permission could place content in the wrong knowledge base.

Mitigation: Confirm the destination Wiki link and Bot edit permissions before writing, and review the created pages after import.

Risk: Browser-profile access may expose visible page content when web_fetch cannot retrieve a complete article.

Mitigation: Use browser-profile access only when needed, ask before attaching if authorization is unclear, and confirm the page body is loaded before extraction.

Risk: Anti-scraping or incomplete page loads can result in missing article content.

Mitigation: Try web_fetch first, fall back to DOM extraction only when necessary, and report permission, network, or extraction failures instead of claiming success.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gift-is-coding/skills/wechat-to-feishu-wiki)
- [Feishu app permission troubleshooting](https://open.feishu.cn/document/faq/trouble-shooting/how-to-add-permissions-to-app?lang=zh-CN&utm_source=chatgpt.com)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown article content plus status text and created page links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates one Feishu Wiki child page per WeChat article link and reports success or failure for each item.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
