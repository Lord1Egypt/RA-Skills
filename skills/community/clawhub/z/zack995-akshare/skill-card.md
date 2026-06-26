## Description: <br>
Use AKShare for Chinese market and macro-finance data via Python. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zack995](https://clawhub.ai/user/Zack995) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to bootstrap an AKShare Python environment, run targeted public-market and macro-finance queries, and summarize the returned data for Chinese equities, funds, indexes, rates, bonds, commodities, futures, and related datasets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The query helper can run arbitrary Python code if it receives a dangerous expression. <br>
Mitigation: Run only trusted expressions, avoid expressions copied from untrusted sources, and prefer a sandboxed environment or a future version with explicit validated AKShare commands. <br>
Risk: AKShare endpoints depend on public upstream data sources that may change or become temporarily unavailable. <br>
Mitigation: Start with narrow queries, report the AKShare method and date range used, and treat endpoint failures or partial results as non-authoritative. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Zack995/zack995-akshare) <br>
- [Publisher profile](https://clawhub.ai/user/Zack995) <br>
- [Homepage from metadata](https://github.com/Zack995) <br>
- [Common AKShare recipes](references/common-recipes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown guidance with inline shell commands; helper output may be CSV, JSON, or text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper prints a limited preview of tabular results by default and can be configured with --max-rows.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
