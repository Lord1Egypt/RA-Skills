## Description: <br>
Scans TRON tokens and TRX for supply, market, price, holder, launch, rating, and transfer-related information using TronScan MCP lookup tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sshnii](https://clawhub.ai/user/sshnii) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to investigate TRON tokens, TRX metrics, holders, supply, market data, and basic token risk signals before summarizing due-diligence findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Token or wallet-address queries are sent to the external TronScan MCP service. <br>
Mitigation: Use the skill only for public TRON token and address research, and do not provide private labels, secrets, seed phrases, API keys, wallet credentials, or addresses that should not be shared with TronScan. <br>
Risk: Token risk, rating, and legitimacy signals can be incomplete or misleading when interpreted alone. <br>
Mitigation: Combine multiple available TronScan signals such as red_tag, tokenCanShow, blueTag, publicTag, vip, tokenLevel, and holder concentration before presenting a safety or official-token conclusion. <br>


## Reference(s): <br>
- [TronScan MCP Server](https://mcp.tronscan.org/mcp) <br>
- [TronScan MCP Guide](https://mcpdoc.tronscan.org) <br>
- [TronScan Developer API](https://tronscan.org/#/developer/api) <br>
- [ClawHub Skill Page](https://clawhub.ai/sshnii/tronscan-token-scanner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown or concise text summaries backed by TronScan MCP tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only external TronScan MCP lookups; no files are produced by the skill.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
