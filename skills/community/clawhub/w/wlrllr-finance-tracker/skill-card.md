## Description: <br>
Tracks personal expenses, monthly budgets, shop purchases, sales, inventory, and profit using local JSON finance records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wlrllr](https://clawhub.ai/user/wlrllr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and small shop operators use this skill to record daily spending, monitor monthly budgets, track purchases and sales, calculate inventory, and generate personal or shop finance reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores detailed spending, budget, inventory, purchase, and sales history in local private-data files. <br>
Mitigation: Use it only in trusted OpenClaw environments and review the local finance data directory before sharing or backing up the workspace. <br>
Risk: Budget checks can produce proactive reminder behavior during heartbeat use. <br>
Mitigation: Review or disable proactive budget reminders if unsolicited finance prompts are not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wlrllr/wlrllr-finance-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with optional shell command invocations and local JSON-backed finance records.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads and writes personal and shop finance data under ~/private_data/openclaw/workspace/data/finance/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
