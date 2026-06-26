## Description: <br>
Converts natural language data requests and provided database schemas into syntactically correct SQL queries, with optional explanations or alternative query strategies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjipeng977](https://clawhub.ai/user/wangjipeng977) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and non-technical users use this skill to turn schema-grounded data questions into SQL queries without inventing table or column names. It is useful when a user provides database schema details and asks for a query, an explained query, or alternative query approaches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated SQL may be incorrect or unsafe to run against production databases or sensitive business data. <br>
Mitigation: Review each query against the provided schema, permissions, and expected data impact before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangjipeng977/text-to-sql) <br>
- [Skill metadata source: MiniMax-AI skills](https://github.com/MiniMax-AI/skills) <br>
- [text-to-sql references](references/index.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown with SQL code blocks and brief explanations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include inline SQL comments or multiple alternative query approaches depending on the selected mode.] <br>

## Skill Version(s): <br>
999.0.0 (source: ClawHub release metadata; artifact metadata lists 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
