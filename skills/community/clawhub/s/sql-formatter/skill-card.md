## Description:

Formats, minifies, and lints SQL queries from the command line with indentation, keyword casing, comment removal, whitespace cleanup, and checks for common SQL anti-patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnywang2001](https://clawhub.ai/user/johnnywang2001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data practitioners use this skill to format SQL files or inline SQL, minify SQL for deployment, and lint queries for common readability and quality issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-specified input and output paths can read or overwrite files the operator did not intend to target.

Mitigation: Review --input and --output paths before execution and provide only files intended for local formatting, minification, or linting.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and generated SQL text or JSON lint output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command output may be written to stdout or to a user-specified output file.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
