## Description: <br>
Converts user-provided natural-language data requests and database schemas into SQL queries, with options to explain the query or provide alternative query strategies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjipeng977](https://clawhub.ai/user/wangjipeng977) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and other users provide an existing database schema plus a plain-language question, and the skill drafts SQL that matches the supplied tables and columns. It can also explain the generated query or compare alternative query strategies for learning and review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Database schemas or table descriptions shared with the agent may reveal sensitive structure or business context. <br>
Mitigation: Share only the schema details needed for the query and avoid including secrets, credentials, or sensitive sample data. <br>
Risk: Generated SQL may be incorrect or unsafe if run directly against a real database. <br>
Mitigation: Review and test generated queries in a safe environment before executing them against production or sensitive data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangjipeng977/text-to-sql-v2) <br>
- [Metadata source: MiniMax-AI skills](https://github.com/MiniMax-AI/skills) <br>
- [Skill references index](references/index.md) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Markdown, Guidance] <br>
**Output Format:** [Markdown with SQL code blocks and brief explanatory text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces SQL for review but does not execute it; asks for schema details when they are missing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
