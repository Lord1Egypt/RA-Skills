## Description:

Fetch and inspect Sina Finance public market data for A-share, Hong Kong stock, and domestic futures symbols, including futures page metadata and Chinese futures name normalization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yonglongjinhao-max](https://clawhub.ai/user/yonglongjinhao-max)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and market analysts use this skill to detect supported Sina Finance market symbols, fetch public quote data, inspect futures page metadata, and summarize A-share, Hong Kong stock, and domestic futures results for informational workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The symbols a user asks the skill to inspect are sent to public Sina Finance resources.

Mitigation: Use the skill only for symbols you are comfortable disclosing to Sina Finance.

Risk: Public webpage resources and unofficial quote fields may change or return incomplete data.

Mitigation: Treat results as informational and verify important quote fields against authoritative market data before making trading, compliance, or financial decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yonglongjinhao-max/skills/sina-market)
- [ClawHub publisher profile](https://clawhub.ai/user/yonglongjinhao-max)
- [Sina futures normalized fields](references/fields.md)
- [Chinese futures mapping](references/chinese_futures_mapping.json)
- [Sina Finance quote endpoint](https://hq.sinajs.cn)
- [Sina Finance futures quote pages](https://finance.sina.com.cn/futures/quotes)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown guidance with inline shell commands; helper scripts can emit JSON or table output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Quote availability and field coverage depend on public Sina Finance webpage resources.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
