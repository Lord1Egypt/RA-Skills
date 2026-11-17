## Description:

Automatically detects scale dimensions from prefix-plus-number column names, computes mean scores for each dimension, and supports reverse scoring and missing-value handling for Excel and CSV inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[y-egg](https://clawhub.ai/user/y-egg)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, analysts, and developers use this skill to score psychology questionnaire or survey spreadsheets by grouping item columns into dimensions, applying optional reverse scoring, and appending computed dimension means to the dataset.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local questionnaire spreadsheets that may contain sensitive respondent data.

Mitigation: Run it only on files approved for local processing and limit access to the input spreadsheet.

Risk: The default _scored output path may overwrite or replace an existing scored file.

Mitigation: Review or explicitly set the output path before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/y-egg/skills/scale-scorer)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Text]

**Output Format:** [CSV or Excel file with added dimension-score columns, plus console text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a local scored output file, using a _scored suffix by default unless an output path is supplied.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
