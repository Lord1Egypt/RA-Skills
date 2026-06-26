## Description: <br>
Runs an AgentScope-based multi-agent stock diagnosis workflow that generates technical, fundamental, sentiment, debate, trader, risk, and final decision reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ganyu21](https://clawhub.ai/user/ganyu21) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and external users use this skill to run a configurable multi-agent Chinese stock diagnosis workflow that gathers market, fundamental, and news data, debates investment views, and produces decision reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Full analysis context can be sent to external services including DashScope and, in batch notification mode, DingTalk. <br>
Mitigation: Use only data approved for those services, and do not provide private portfolio, client, or confidential research data unless that sharing is acceptable. <br>
Risk: Streamed model reasoning or intermediate analysis can be printed into logs. <br>
Mitigation: Disable background logging for sensitive runs, or sanitize logs before retention or sharing. <br>
Risk: Normal use may install or rely on Python packages at runtime. <br>
Mitigation: Run the skill in an isolated Python environment and review or pin dependencies before deployment. <br>
Risk: Generated outputs may look like trading recommendations. <br>
Mitigation: Treat outputs as research assistance and require qualified human review before making financial decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ganyu21/trading-agents) <br>
- [DashScope-compatible OpenAI endpoint](https://dashscope.aliyuncs.com/compatible-mode/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, PDF, Shell commands, Configuration] <br>
**Output Format:** [Markdown reports, JSON diagnosis data, PDF report, and command/configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires stock-code input and API credentials; batch mode can process multiple stocks.] <br>

## Skill Version(s): <br>
1.0.7 (source: ClawHub release metadata; artifact package metadata reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
