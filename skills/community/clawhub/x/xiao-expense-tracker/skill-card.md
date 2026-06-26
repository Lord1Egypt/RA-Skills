## Description: <br>
A personal expense-tracking skill for recording income and spending, categorizing transactions, managing budgets, and exporting reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaising-openclaw1](https://clawhub.ai/user/kaising-openclaw1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to track personal income and expenses, review category and monthly statistics, set budgets, and export financial reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may handle sensitive income, spending, budget, account, and exported report data. <br>
Mitigation: Treat finance records and exports as sensitive and verify where records are stored or exported before use. <br>
Risk: The artifact declares a curl binary requirement without explaining why it is needed. <br>
Mitigation: Clarify the curl requirement before relying on the skill in a sensitive finance workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaising-openclaw1/xiao-expense-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference income, spending, budget, account, and exported report data that should be treated as sensitive.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
