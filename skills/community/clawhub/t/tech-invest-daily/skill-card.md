## Description:

生成科技行业投资日报，抓取财联社科技新闻和相关上市公司股价，产出深度分析报告并通过飞书发送 Markdown 与 PDF 附件。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ilove323](https://clawhub.ai/user/ilove323)

### License/Terms of Use:


## Use Case:

External users and scheduled automation workflows use this skill to collect technology-sector news, retrieve related public-company price data, and produce a daily investment report for delivery through Feishu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports and PDF attachments are sent to a fixed Feishu recipient without adequate user control.

Mitigation: Use only where that recipient is intended, or require recipient confirmation before every send.

Risk: The workflow accesses central Feishu app credentials from /root/.openclaw/openclaw.json.

Mitigation: Run only in environments where those credentials are safe for agent-executed code to access; prefer platform-managed messaging credentials.

Risk: Market data is fetched through an unauthenticated HTTP quote endpoint.

Mitigation: Prefer HTTPS and authenticated market data sources before using reports for operational decisions.

Risk: Markdown-to-PDF rendering processes generated report content.

Mitigation: Sandbox PDF rendering and review generated files before distribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ilove323/skills/tech-invest-daily)
- [财联社电报实时新闻流](https://www.cls.cn/telegraph)
- [财联社新闻详情](https://www.cls.cn/detail/{id})
- [腾讯行情接口](http://qt.gtimg.cn/q=代码1,代码2)
- [Feishu Open Platform message API](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown report with JSON stock quote data and PDF attachment workflow]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write temporary Markdown/PDF files under /tmp and send a Markdown message plus PDF attachment through Feishu.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
