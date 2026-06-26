## Description: <br>
Manage Steven's A-share shadow trading dashboard, including simulated trades, positions, equity data, trade history, and local dashboard files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[j97feng-beep](https://clawhub.ai/user/j97feng-beep) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Traders or portfolio reviewers use this skill to maintain a local simulated A-share trading dashboard, update trade records, recalculate portfolio metrics, and open the dashboard after changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated trade records, prices, fees, cash balances, equity, or history may be inaccurate. <br>
Mitigation: Review generated dashboard and data-file changes before relying on the simulated portfolio. <br>
Risk: The skill writes to local trade and dashboard files. <br>
Mitigation: Install and run it only in workspaces where an agent should maintain those local files. <br>


## Reference(s): <br>
- [Shadow Trading Dashboard on ClawHub](https://clawhub.ai/j97feng-beep/shadow-trading-dashboard) <br>
- [Publisher profile](https://clawhub.ai/user/j97feng-beep) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with file updates and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local dashboard, metrics, position, order, trade history, and equity curve files under trade/.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
