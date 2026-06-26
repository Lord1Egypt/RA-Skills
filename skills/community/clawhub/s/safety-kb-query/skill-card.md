## Description: <br>
Queries a local safety-regulation SQLite knowledge base to search regulations, check standard coverage, inspect clauses, report database statistics, inspect schema, and detect data quality issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyz9827](https://clawhub.ai/user/cyz9827) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to query the safety-review knowledge base for safety standards, regulation clauses, coverage gaps, database statistics, and data quality checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper queries whichever readable SQLite database is selected by KB_PATH or the default path. <br>
Mitigation: Verify KB_PATH before use, especially on shared machines, and install only when the agent should read the safety-review SQLite database. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cyz9827/safety-kb-query) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled helper emits JSON for search, check, info, clauses, stats, schema, and conflicts commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
