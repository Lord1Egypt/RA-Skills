## Description: <br>
Analyzes A-share stock themes, clusters related concepts, searches recent finance and news events, and generates a Markdown report linking themes to market-moving events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shinelp100](https://clawhub.ai/user/shinelp100) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, and market-analysis users can use this skill to connect recent A-share stock-theme clusters with supporting news events and produce a structured daily-review report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may access external market and news services while collecting finance context. <br>
Mitigation: Run it only in environments where those external requests are acceptable, and review generated reports before relying on them. <br>
Risk: The skill may write report and cache files to local paths selected during execution. <br>
Mitigation: Review the output path before running and restrict execution to a workspace where generated files are expected. <br>
Risk: The skill may download Python or model dependencies and invoke a related stock-theme lookup subagent. <br>
Mitigation: Install dependencies from trusted package sources and review subagent usage before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shinelp100/stock-theme-events) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with structured tables and supporting JSON-style analysis data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local report and cache files, query external market/news services, and invoke a related stock-theme lookup subagent.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
