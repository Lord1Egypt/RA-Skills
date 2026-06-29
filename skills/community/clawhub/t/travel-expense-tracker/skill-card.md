## Description: <br>
旅行场景专项记账助手；多币种记录消费、汇率自动换算、分类统计与预算管理。当用户需要记录旅行花费、多币种换算记账、旅行预算管理、分类统计旅行支出时使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[travel-skills](https://clawhub.ai/user/travel-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and agents assisting travelers use this skill to record trip expenses, convert supported currencies to CNY with built-in reference rates, summarize spending, and check trip budgets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trip names, dates, amounts, categories, and descriptions can reveal private travel and financial details because records are saved as local JSON files. <br>
Mitigation: Use the skill on trusted devices, review the travel_expenses/ directory, and delete records when they are no longer needed. <br>
Risk: Converted CNY amounts use built-in reference exchange rates, so they may not match current rates or card statement totals. <br>
Mitigation: Treat converted totals as planning estimates and verify exchange rates or statements before making financial decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/travel-skills/travel-expense-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [Natural-language responses based on JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores and reads trip expense JSON files under travel_expenses/.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
