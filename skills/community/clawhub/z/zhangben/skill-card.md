## Description: <br>
账本 helps agents manage personal bookkeeping and assets through the Taozhu Zhangben MCP interface for income, expenses, asset trades, liabilities, transactions, and wealth summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chensenym](https://clawhub.ai/user/chensenym) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and their agents use this skill to record and review personal financial activity, including income, expenses, assets, liabilities, transactions, and wealth summaries via the Taozhu Zhangben MCP service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive financial records and credentials with under-scoped authentication and write-operation safeguards. <br>
Mitigation: Review before installing, prefer the user-provided token path, treat saved tokens and identity IDs as sensitive credentials, and require explicit user confirmation before financial write operations. <br>
Risk: The API identity path can create device-linked identification. <br>
Mitigation: Avoid the MAC-derived API identity path unless the user accepts device-linked identification, and preserve the generated identity ID only when that authentication mode is chosen. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chensenym/zhangben) <br>
- [Authentication flow](references/auth.md) <br>
- [MCP API reference](references/mcp-api.md) <br>
- [Category codes](references/category-codes.md) <br>
- [Platform IDs](references/platform-ids.md) <br>
- [Common error codes](references/errorcode.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, API calls] <br>
**Output Format:** [Markdown guidance with JSON-RPC tool-call examples and parameter schemas] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-selected authentication and handles sensitive personal finance data and tokens.] <br>

## Skill Version(s): <br>
1.0.2 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
