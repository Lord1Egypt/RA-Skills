## Description:

全网持续收录每日超过1000+公众号10w+文章内容，向用户推送公众号达到10w+阅读的热门文章；当用户需要获取全领域的公众号热门文章、或订阅每日10w+文章推送、特定领域爆款文章时使用

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

WeChat editors, content creators, media operators, and marketing teams use this skill to retrieve recent WeChat Official Account 10w+ article rankings, inspect category-specific viral content, analyze repeatable viral patterns, and generate shareable HTML reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports can include unsafe browser code from external article data.

Mitigation: Open generated reports only when the data source is trusted, review or sanitize report fields before sharing, and prefer a fixed version that escapes all report fields and validates URLs.

Risk: The fetch script prints part of the RedFox API key in command output.

Mitigation: Treat command output and logs as sensitive, avoid sharing them, and prefer a fixed version that removes API-key prefix logging; rotate the key if exposure is suspected.

Risk: Generated reports load html2pdf.js from a CDN.

Mitigation: Use the report in environments that permit the external CDN dependency, or prefer a fixed version that vendors the script or pins it with integrity checks.

Risk: Command output may include an unsolicited sales contact message.

Mitigation: Review output before forwarding it to end users and prefer a fixed version that removes nonessential promotional text.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/wechat-10w-hot)
- [API specification](artifact/references/api-spec.md)
- [Category mapping](artifact/references/category-mapping.md)
- [RedFox API key settings](https://redfox.hk/settings/api-keys?source=clawhub)

## Skill Output:

**Output Type(s):** [text, markdown, HTML, shell commands, configuration, guidance]

**Output Format:** [Markdown article tables and analysis, shell command snippets, JSON-backed temporary article data, and generated HTML reports with PDF export support.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REDFOX_API_KEY and uses recent WeChat article data returned by the RedFox API.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
