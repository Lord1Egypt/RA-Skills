## Description: <br>
Expense Tracker helps users log spending, track income, manage budgets, set savings goals, split bills, view spending reports, export financial data, and receive spending insights from natural-language chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mkpareek0315](https://clawhub.ai/user/mkpareek0315) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill as a chat-based personal finance assistant for recording expenses and income, reviewing spending patterns, managing budgets, tracking recurring payments, and monitoring savings goals with local data storage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill has a broad activation scope for a finance assistant that can create and update persistent personal expense records. <br>
Mitigation: Review before installing, enable it only for users comfortable with a local finance tracker, and require clear confirmation before first-run setup or state-changing actions. <br>
Risk: Persistent local expense, income, budget, recurring-payment, goal, and settings files may be changed or deleted during normal use. <br>
Mitigation: Keep the built-in backup behavior enabled, review destructive actions before confirming them, and inspect exported or updated finance data before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mkpareek0315/smart-expense-tracker) <br>
- [Publisher social profile](https://x.com/Mkpareek19_) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Conversational Markdown with occasional shell snippets, JSON records, and CSV export output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local finance data files under the user's expense-tracker directory; no external API or network output is described in the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
