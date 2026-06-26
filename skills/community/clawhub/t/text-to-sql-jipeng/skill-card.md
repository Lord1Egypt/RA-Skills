## Description: <br>
Converts natural-language data requests with a provided database schema into SQL queries, explanations, or alternative query approaches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjipeng977](https://clawhub.ai/user/wangjipeng977) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and external users use this skill to turn schema-grounded natural-language questions into SQL. It is intended for drafting and explaining queries, not for executing SQL or analyzing returned data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated SQL may be syntactically valid but semantically wrong for a user's database or business question. <br>
Mitigation: Review the query against the provided schema and intended result before execution. <br>
Risk: Running generated queries directly against production or sensitive databases could expose data or cause operational issues. <br>
Mitigation: Test queries in a safe environment and apply normal database access controls before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangjipeng977/text-to-sql-jipeng) <br>
- [Publisher profile](https://clawhub.ai/user/wangjipeng977) <br>
- [MiniMax-AI skills source listing](https://github.com/MiniMax-AI/skills) <br>
- [text-to-sql references index](references/index.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown with SQL code blocks and concise explanations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs drafted SQL only; users should review generated queries before running them against real databases.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter and changelog also mention 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
