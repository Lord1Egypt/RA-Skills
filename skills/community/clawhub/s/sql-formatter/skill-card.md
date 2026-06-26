## Description: <br>
Format, minify, and lint SQL queries from the command line with configurable indentation, keyword casing, comment removal, and checks for common SQL anti-patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Johnnywang2001](https://clawhub.ai/user/Johnnywang2001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to format SQL files or inline queries, minify SQL for production use, and lint SQL for common quality issues before review or execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read from input paths and write to output paths supplied by the user. <br>
Mitigation: Check --input and --output paths before running commands so only intended SQL files are read or written. <br>
Risk: Automated SQL formatting or minification may change readability or expose query issues that still require human review. <br>
Mitigation: Review formatted or minified SQL before using it in production workflows. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and command output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can emit formatted SQL text, minified SQL text, lint messages, or JSON lint output depending on the selected command.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
