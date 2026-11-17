## Description:

全网持续收录每日公众号原创热门文章内容，向用户推送公众号原创热门文章；当用户需要获取全领域的公众号原创热门文章、或订阅每日原创热门文章推送时使用

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanyi-github](https://clawhub.ai/user/yuanyi-github)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, editors, content planners, and operations teams use this skill to query original viral WeChat Official Account article rankings by category or date, review the returned article table, generate an HTML/PDF-ready report, and request daily category subscription pushes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends authenticated requests to the RedFox API and depends on REDFOX_API_KEY handling.

Mitigation: Install only when the RedFox integration is trusted, keep the key in environment configuration, confirm key scope and revocation, and avoid exposing it in prompts, logs, code, or generated files.

Risk: Remote article fields and URLs are displayed in Markdown and may be used in generated HTML/PDF reports.

Mitigation: Escape and validate article fields and links before display or report generation, and review generated reports before sharing or opening them in sensitive environments.

Risk: The security guidance says normal TLS verification should be restored before real API-key use.

Mitigation: Require standard certificate and hostname verification for API calls before using production credentials.

Risk: The skill can create local report files and prompts for subscription behavior.

Mitigation: Make HTML/PDF generation and subscription actions explicit and user-controlled before creating files or enabling recurring pushes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanyi-github/skills/wechat-original-hot)
- [Category mapping reference](references/category_mapping.md)
- [RedFoxHub API key settings](https://redfox.hk/settings/api-keys?source=clawhub)
- [RedFox data API endpoint](https://redfox.hk/story/api/cozeSkill/getWxDataByCategoryAndTime)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML, Configuration, Guidance]

**Output Format:** [Markdown article ranking tables, subscription prompts, and optional generated HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REDFOX_API_KEY and may create local JSON and HTML report files.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
