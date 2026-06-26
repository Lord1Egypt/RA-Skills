## Description: <br>
科技行业投资日报生成与推送。当用户要求生成科技投资日报、发送每日投资报告、或cron定时触发日报任务时使用。自动抓取财联社实时新闻、获取涉及上市公司股价、生成深度分析报告并通过飞书一条消息发送完整Markdown报告，同时生成PDF附件。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ilove323](https://clawhub.ai/user/ilove323) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and analysts use this skill to generate Chinese-language daily technology investment reports from current news and market-price data. It can prepare a Markdown report, create a PDF attachment, and send the report through Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use stored Feishu app credentials to send generated reports and PDF files to a fixed recipient. <br>
Mitigation: Confirm the recipient before use, restrict Feishu credentials to the minimum message and file permissions, and require approval before scheduled or automatic sends. <br>
Risk: The report includes generated market analysis and investment suggestions. <br>
Mitigation: Treat the output as informational, require human review, and do not use it as sole basis for investment decisions. <br>
Risk: PDF generation depends on external conversion tooling. <br>
Mitigation: Verify the PDF converter dependency and execution path before enabling report attachment delivery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ilove323/tech-invest-daily) <br>
- [财联社实时新闻流](https://www.cls.cn/telegraph) <br>
- [财联社新闻详情](https://www.cls.cn/detail/{id}) <br>
- [腾讯行情数据接口](http://qt.gtimg.cn/q=代码1,代码2) <br>
- [Feishu tenant access token endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu file upload endpoint](https://open.feishu.cn/open-apis/im/v1/files) <br>
- [Feishu message send endpoint](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown investment report, JSON stock-price data, and PDF attachment] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated market analysis is informational and should not be treated as financial advice.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
