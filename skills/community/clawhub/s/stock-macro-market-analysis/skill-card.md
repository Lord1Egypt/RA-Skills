## Description: <br>
Analyzes A-share, U.S., and Hong Kong market trends, sentiment, capital flows, macroeconomic conditions, policy effects, and sector rotation to generate a market overview report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuritu](https://clawhub.ai/user/wuritu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, investors, analysts, and agent operators use this skill to produce structured market analysis across technical indicators, breadth, fund flows, sentiment, macro data, policy, and global market linkage. The generated reports support research and review workflows and should not be treated as financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated market recommendations can be incorrect, incomplete, or mistaken for financial advice. <br>
Mitigation: Require human review before acting on outputs, preserve source and timestamp labels, and keep the skill's disclaimer in generated reports. <br>
Risk: The skill may run local Python market-analysis tools and use a stock-data API key. <br>
Mitigation: Use a dedicated, revocable API key where possible and review any helper scripts before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wuritu/stock-macro-market-analysis) <br>
- [Publisher Profile](https://clawhub.ai/user/wuritu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown market analysis reports with JSON snippets and inline shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are expected to include data sources, timestamps, confidence labels, and a disclaimer.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and OpenClaw metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
