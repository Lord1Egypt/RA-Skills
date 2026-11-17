## Description: <br>
Provides single-ticker Vegas Channel technical analysis, including trend identification, basic buy/sell signals, and support and resistance levels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Personal traders and agent users use this skill to request informational technical analysis for one ticker at a time. It helps summarize Vegas Channel trend posture, basic trade signals, and key price levels without providing automated trading execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests read, write, and shell execution authority that is broader than its free analysis-only purpose requires. <br>
Mitigation: Install and run it only in controlled workspaces, and review proposed shell commands and file writes before execution. <br>
Risk: Callback URL support may send analysis results to an external endpoint. <br>
Mitigation: Avoid providing callback URLs unless the endpoint is trusted and external delivery is expected. <br>
Risk: Trading signals and technical analysis may be incorrect, delayed, or misleading. <br>
Mitigation: Treat outputs as informational analysis, not financial advice, and verify conclusions independently before making trading decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/trading-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and structured analysis text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are informational trading analysis and should not be treated as financial advice.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
