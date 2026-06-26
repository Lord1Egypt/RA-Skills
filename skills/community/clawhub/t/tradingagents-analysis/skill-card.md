## Description: <br>
A股多智能体投研-15 AI 分析师 submits China A-share symbols to the TradingAgents API and returns multi-agent technical, fundamental, sentiment, capital-flow, macro, and risk analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kylinmountain](https://clawhub.ai/user/kylinmountain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to request China A-share stock research from a hosted or self-hosted TradingAgents backend. It is intended to provide structured buy, sell, or hold research support with risk assessment, not guaranteed financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends requested A-share symbols and analysis parameters to a TradingAgents backend using a bearer token. <br>
Mitigation: Install only when the user trusts the hosted backend or has configured a trusted self-hosted TRADINGAGENTS_API_URL, and protect TRADINGAGENTS_TOKEN as an API credential. <br>
Risk: Analysis output may include buy, sell, or hold recommendations that could be mistaken for guaranteed financial advice. <br>
Mitigation: Treat results as research support, review assumptions independently, and avoid including account details or exact private holdings in prompts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kylinmountain/tradingagents-analysis) <br>
- [TradingAgents app homepage](https://app.510168.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with JSON analysis results from shell/API calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TRADINGAGENTS_TOKEN and supports TRADINGAGENTS_API_URL for a trusted self-hosted backend.] <br>

## Skill Version(s): <br>
0.6.2 (source: server release metadata; artifact frontmatter reports 0.6.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
