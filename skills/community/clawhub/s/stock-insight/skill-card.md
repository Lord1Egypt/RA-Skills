## Description: <br>
Stock Insight guides an agent to produce Chinese-language stock research reports using current market data checks, structured analysis, and actionable scenarios. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[karlinmoon](https://clawhub.ai/user/karlinmoon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, investors, and analysts use this skill to request concise stock research in Chinese. The agent gathers current market, fundamental, industry, fund-flow, and technical signals, then returns a stance, score, and concrete watch or action scenarios with risk language. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce concrete buy, sell, target-price, stop-loss, and position-sizing suggestions that users may mistake for personalized financial advice. <br>
Mitigation: Present outputs as informational analysis, include clear risk language, and require users to verify decisions independently against their own circumstances and qualified advice. <br>
Risk: Stock analysis can become misleading when market, financial, or industry data is stale, incomplete, or not source-labeled. <br>
Mitigation: Use current market data, label source and retrieval time for key figures, and explicitly mark unavailable data instead of estimating it. <br>
Risk: Broad Chinese trigger phrases may activate the skill when the user did not intend a full stock research workflow. <br>
Mitigation: Narrow activation triggers or ask a clarifying question when accidental activation would be disruptive. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/karlinmoon/stock-insight) <br>
- [Industry leading indicators](references/industry-leading-indicators.md) <br>
- [Analysis examples](references/analysis-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Chinese Markdown stock research report with dated data notes, a core stance, four-part analysis, score, and actionable scenarios.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires current market data and source/time labels; outputs should be treated as informational analysis, not personalized financial advice.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
