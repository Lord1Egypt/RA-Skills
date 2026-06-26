## Description: <br>
Tracks personal expenses in local JSON files and provides command-line workflows for adding expenses, querying spending, checking budgets, generating reports, summarizing locations, producing snarky spending analysis, and creating trend charts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ybl2020](https://clawhub.ai/user/ybl2020) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to maintain a personal spending ledger, review budget status, summarize expense patterns, and generate local reports or trend charts from recorded expense data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trend chart generation can send spending totals to OpenRouter when OPENROUTER_API_KEY is configured. <br>
Mitigation: Leave OPENROUTER_API_KEY unset or avoid the trend feature unless sharing spending totals with OpenRouter is acceptable. <br>
Risk: Expense and location history is stored in local JSON files selected by environment variables. <br>
Mitigation: Set EXPENSE_DATA_FILE and EXPENSE_TRENDS_DIR to intended private paths and use appropriate filesystem permissions before recording sensitive personal data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ybl2020/snarky-expense-butler) <br>
- [Publisher Profile](https://clawhub.ai/user/ybl2020) <br>
- [OpenRouter Chat Completions API](https://openrouter.ai/api/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown or plain text with shell commands, local JSON data, and optional PNG trend chart files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local expense JSON files by default; trend chart generation may call OpenRouter when OPENROUTER_API_KEY is configured, otherwise it falls back to matplotlib.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
