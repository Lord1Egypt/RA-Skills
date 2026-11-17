## Description:

全网持续收录每日公众号原创热门文章内容，向用户推送公众号原创热门文章；当用户需要获取全领域的公众号原创热门文章、或订阅每日原创热门文章推送时使用

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, WeChat account operators, planners, and analysts use this skill to retrieve ranked original WeChat Official Account articles by category or date, review trends, and generate shareable HTML/PDF-style reports. It can also support daily subscription-style tracking of original viral article rankings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a RedFox API key and the security evidence flags insecure key handling.

Mitigation: Use a low-scope, revocable key; configure it only through environment variables; avoid exposing it in prompts, logs, code, or generated files; and rotate it if exposure is suspected.

Risk: The security evidence says TLS verification is not fixed for the API request path.

Mitigation: Review the script before installation and avoid using the skill on untrusted networks until TLS certificate verification is corrected.

Risk: Generated HTML reports may include unescaped remote article data and are opened in a browser context.

Mitigation: Open generated reports only when the article data source is trusted, and avoid opening reports produced from tampered or untrusted data.

Risk: The skill creates local JSON and HTML files and may include RedFox promotional text in user-facing output.

Mitigation: Run it in a workspace where generated files are expected, review outputs before sharing, and remove promotional content if it is inappropriate for the deployment context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/wechat-original-article-king)
- [RedFoxHub API key settings](https://redfox.hk/settings/api-keys?source=clawhub)
- [RedFoxHub](https://redfox.hk?source=clawhub)
- [Article ranking API endpoint](https://redfox.hk/story/api/cozeSkill/getWxDataByCategoryAndTime)
- [Category mapping](references/category_mapping.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown article ranking tables plus generated local JSON and HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REDFOX_API_KEY; rankings are snapshots from RedFox data and may vary from live WeChat read counts.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
