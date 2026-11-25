## Description:

微信搜一搜公开数据只读：按关键词搜微信文章、微信视频。触发：微信搜索、搜一搜、公众号文章、视频号、微信热门、微信最新、wechat search、wechat article、wechat video。抖音、小红书、快手、B站、微博不要用本技能。不支持图片搜索、正文抓取、账号登录。

This skill is ready for commercial/non-commercial use.

## Publisher:

[um-why](https://clawhub.ai/user/um-why)

### License/Terms of Use:

MIT

## Use Case:

Developers and content analysts use this skill to search public WeChat articles and videos by keyword for topic discovery, competitor analysis, and trend monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords are sent to the external Guaikei API.

Mitigation: Avoid using sensitive or private terms as search keywords.

Risk: The security scan had partial coverage, so its benign verdict does not resolve all uncertainty.

Mitigation: Review the skill code and consider the scan's stated coverage limits before installation.

## Reference(s):

- [Skill release page](https://clawhub.ai/um-why/skills/wechat-search-sou)
- [Search options](references/options.md)
- [Output contract](references/contract.md)
- [Environment and usage FAQ](references/faq.md)
- [Guaikei service](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON]

**Output Format:** [JSON output envelope containing structured article or video search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only search results; the envelope can also report empty or error states, and may include an estimated cost.]

## Skill Version(s):

1.1.3 (source: SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
