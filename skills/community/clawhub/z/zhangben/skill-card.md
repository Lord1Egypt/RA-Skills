## Description:

Zhangben helps agents manage personal bookkeeping and assets through the Taozhu Zhangben MCP interface, including income, expenses, asset trades, liabilities, transactions, and dashboard summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chensenym](https://clawhub.ai/user/chensenym)

### License/Terms of Use:

MIT-0

## Use Case:

External users and personal finance agents use this skill to authenticate with moneydata.cn, record income and expenses, manage asset and liability transactions, and query financial summaries. It is intended for personal bookkeeping workflows where the user can confirm financial write actions before they are sent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Personal financial records and authentication material are sent to moneydata.cn.

Mitigation: Install only if that service is acceptable for the user's financial data, and prefer an authentication path the user understands before any financial action is taken.

Risk: The automatic API authentication path can create a persistent device identifier from the user's MAC address.

Mitigation: Prefer the user-provided WeChat mini-program token when possible; use the automatic API path only if persistent device linkage is acceptable.

Risk: The skill can guide write actions that record or change income, expenses, assets, debts, and repayments.

Mitigation: Require user confirmation of tool name, amount, currency, platform, category, and date before submitting any write operation.

## Reference(s):

- [Authentication Flow](references/auth.md)
- [MCP API Reference](references/mcp-api.md)
- [Category Codes](references/category-codes.md)
- [Platform IDs](references/platform-ids.md)
- [Error Codes](references/errorcode.md)
- [Taozhu Zhangben MCP endpoint](https://moneydata.cn/mcp)
- [Taozhu Zhangben token endpoint](https://moneydata.cn/api/user/token)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code examples, shell-command guidance, and JSON-RPC/API call parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires authentication material for moneydata.cn and can guide write actions that record or change financial data.]

## Skill Version(s):

1.0.2 (source: frontmatter, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
