## Description: <br>
Generates real-time China A-share sector research briefs by combining public market data, sector news, US-market linkage, event reminders, and concise markdown reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xujianbo0426](https://clawhub.ai/user/xujianbo0426) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to ask for China A-share sector briefs, AI-market news summaries, and market-movement alerts. It returns markdown summaries grounded in public market and news data, with investment-advice disclaimers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local Node.js scripts that contact external financial and news services. <br>
Mitigation: Review the scripts and network destinations before deployment, and run the skill in an environment approved for market/news lookups. <br>
Risk: Optional Tavily integration requires an API key. <br>
Mitigation: Use a dedicated or rotatable Tavily key and avoid sharing the environment with unrelated workloads. <br>
Risk: Generated stock commentary can be mistaken for investment advice. <br>
Mitigation: Preserve the skill's informational-use disclaimers and require human review before using outputs for financial decisions. <br>
Risk: Generated report data is saved in the artifact's local output directory. <br>
Mitigation: Treat local outputs as public report data and clear or isolate the directory according to workspace retention requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xujianbo0426/stockselectionmodel-bak) <br>
- [Publisher profile](https://clawhub.ai/user/xujianbo0426) <br>
- [Data source list](references/source_list.md) <br>
- [Stock mapping reference](references/stock_mapping.md) <br>
- [Sector analysis prompt](references/sector_prompt.md) <br>
- [AI news analysis prompt](references/analysis_prompt.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports and JSON script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Pretty mode prints markdown directly; JSON mode includes generated markdown plus supporting market, news, and stock data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence; artifact frontmatter says 3.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
