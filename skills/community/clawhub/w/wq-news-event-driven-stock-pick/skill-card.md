## Description:

新闻流事件驱动选股系统 - 接收财经新闻输入，通过百度千帆API进行事件NLP分析，关联受益A股标的，输出事件驱动选股信号。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenxyzcyxpp](https://clawhub.ai/user/chenxyzcyxpp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and finance-focused agents use this skill to turn financial news or policy text into structured A-share event classifications, affected sectors, beneficiary stock candidates, risk factors, and a Markdown-ready analysis report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial news text may be sent to Baidu Qianfan for analysis.

Mitigation: Require explicit user confirmation before sending content to the third-party API and avoid confidential, embargoed, or otherwise sensitive inputs.

Risk: The documented dashboard deployment exposes a public analysis endpoint and the security review calls out plaintext, unauthenticated service exposure.

Mitigation: Serve the dashboard over HTTPS and add authentication, rate limits, and request body-size limits to /api/analyze before production use.

Risk: The deployment guidance includes root-based server update commands.

Mitigation: Use a least-privileged deploy account and restrict deployment credentials to only the required files and service restart operation.

Risk: Generated stock-picking signals can be incorrect, incomplete, or mistaken for investment advice.

Mitigation: Keep the non-investment-advice disclaimer, require human review, and verify signals against independent market and company data before acting.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/chenxyzcyxpp/skills/wq-news-event-driven-stock-pick)
- [Publisher profile](https://clawhub.ai/user/chenxyzcyxpp)
- [Event taxonomy](references/event_taxonomy.md)
- [Web dashboard setup](references/web-dashboard-setup.md)
- [Output report template](templates/output_template.md)
- [Baidu Qianfan chat completions endpoint](https://qianfan.baidubce.com/v2/chat/completions)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON analysis from the script, plus Markdown report text and shell-command/configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires financial/news text and QIANFAN_API_KEY; analysis may send input text to Baidu Qianfan and should retain investment-risk disclaimers.]

## Skill Version(s):

1.0.0 (source: server release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
