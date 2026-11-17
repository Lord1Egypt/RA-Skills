## Description:

Converts pasted PySpark .show() output into tab-separated text that can be copied directly into Excel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dilicloud11](https://clawhub.ai/user/dilicloud11)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to reformat PySpark .show() table output into tab-separated rows for Excel without analyzing or changing the data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad spreadsheet-formatting trigger phrases may invoke the skill for inputs that are not PySpark .show() tables.

Mitigation: Use it with explicit PySpark .show() output and review the tab-separated result before pasting into Excel.

Risk: The skill formats table text only and does not validate, analyze, or correct the underlying data.

Mitigation: Perform any data validation or analysis separately before relying on the pasted spreadsheet content.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown]

**Output Format:** [Markdown code block containing tab-separated text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Removes PySpark table border lines and trailing only-showing row notices; preserves the table content as formatted text.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
