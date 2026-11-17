## Description:

青虎AI 电商选品上货总入口，帮助 agents use Qinghu e-commerce data workflows for product sourcing, competitor analysis, keyword research, market assessment, supplier collection, and listing across Amazon, TikTok Shop, Shopee, Ozon, Douyin, Xiaohongshu, Bilibili, and 1688.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External commerce operators and agents use this skill to route e-commerce sourcing, competitor analysis, market research, supplier discovery, and listing workflows through Qinghu data interfaces. It is intended for product and market decisions across marketplace and social-commerce platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External Qinghu API calls use user-provided credentials and may consume Qinghu credits.

Mitigation: Before approving tool use, confirm the listed tools, expected credit cost, and target platform or account.

Risk: Listing workflows may publish or edit e-commerce listings.

Mitigation: Confirm the destination account, platform, template, and requested action before any publish or edit step.

Risk: Marketplace and social-commerce data can differ from a platform's own back-office reporting.

Mitigation: Use Qinghu data for sourcing and analysis, and confirm high-impact business decisions against authoritative platform account data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/autoagc/skills/qinghu-ecom-sourcing)
- [Qinghu MCP API Endpoint](https://www.iqinghu.com/api/desktop/qh/mcp)
- [Qinghu API Keys](https://www.iqinghu.com/workbench/dashboard/api-keys)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON request examples, shell/API call examples, concise conclusions, and optional exported table files for larger result sets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call external Qinghu HTTP APIs with user-provided credentials and may produce file links for exported datasets.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
