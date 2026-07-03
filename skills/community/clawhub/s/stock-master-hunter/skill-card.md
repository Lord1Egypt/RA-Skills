## Description: <br>
StockMasterHunter helps agents combine Elliott Wave analysis, volume-price dynamics, trend-cycle analysis, 100-bagger fundamental screening, market data, IMA knowledge-base retrieval, and backtesting to produce structured stock analysis and entry/exit guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yjkj999999](https://clawhub.ai/user/yjkj999999) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External investors, analysts, and developers use this skill to turn a general-purpose agent into a structured stock-analysis assistant that screens companies, evaluates technical trend position, runs backtests, and drafts Markdown reports with risk-aware entry, target, and stop-loss conditions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use IMA credentials and external financial or knowledge-base APIs. <br>
Mitigation: Use scoped managed secrets, review the configured data sources, and require confirmation before calls that expose credentials or sensitive queries. <br>
Risk: The skill can persist or modify local knowledge and version files during knowledge-base sync workflows. <br>
Mitigation: Require confirmation before sync or write operations and review diffs before accepting generated knowledge-base or version changes. <br>
Risk: Stock analysis and entry/exit guidance can be incorrect, stale, or misleading if market data is unavailable or incomplete. <br>
Mitigation: Prefer live or user-provided market data, clearly state source limitations, and treat outputs as analysis requiring independent review rather than guaranteed investment advice. <br>


## Reference(s): <br>
- [StockMasterHunter ClawHub listing](https://clawhub.ai/yjkj999999/skills/stock-master-hunter) <br>
- [IMA Agent Interface](https://ima.qq.com/agent-interface) <br>
- [IMA Search Knowledge API](https://ima.qq.com/openapi/wiki/v1/search_knowledge) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown reports with tables, structured text diagrams, inline code examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call external market-data or knowledge-base APIs when configured; should state data limitations when live data is unavailable.] <br>

## Skill Version(s): <br>
2.1.0 (source: frontmatter and ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
