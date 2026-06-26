## Description: <br>
Orchestrates specialized subagents that simulate a trading firm to analyze public securities and produce AI-generated trading research and recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huahang](https://clawhub.ai/user/huahang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run a multi-agent market research workflow for specific tickers, combining fundamental, technical, sentiment, news, debate, risk, and portfolio perspectives. Outputs are research aids and should not be treated as financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can launch many subagents and may incur substantial compute or token cost. <br>
Mitigation: Run one ticker at a time, keep debate rounds low unless needed, and confirm expected cost before starting broad analyses. <br>
Risk: The skill runs local Python market-data commands using user-provided ticker text. <br>
Mitigation: Use simple ticker symbols, review commands before execution, and run the skill in a dedicated workspace. <br>
Risk: The workflow writes multiple reports and data files into the workspace without clear overwrite safeguards. <br>
Mitigation: Use a fresh project or output folder for each analysis and review generated files before relying on them. <br>
Risk: The generated trading recommendation may be incorrect, stale, or unsuitable for a user's financial situation. <br>
Mitigation: Treat outputs as research rather than financial advice and verify decisions against primary sources and qualified professional guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huahang/trading-agents-skill) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/huahang) <br>
- [TradingAgents paper (arXiv 2412.20138)](https://arxiv.org/abs/2412.20138) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON data files, and conversational text summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes multiple analysis files to the workspace, including a comprehensive report and debate record.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
